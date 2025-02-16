from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, avg, udf, from_unixtime
from pyspark.sql.types import StructType, StructField, StringType, DoubleType
from textblob import TextBlob

# Define the schema to match your JSON messages.
schema = StructType([
    StructField("id", StringType(), True),
    StructField("title", StringType(), True),
    StructField("selftext", StringType(), True),
    StructField("created_utc", DoubleType(), True),
    StructField("url", StringType(), True),
    StructField("author", StringType(), True)
])

# Define a UDF for sentiment analysis using TextBlob.
def get_sentiment(text):
    try:
        return TextBlob(text).sentiment.polarity
    except Exception:
        return 0.0

# Register the UDF with Spark.
sentiment_udf = udf(get_sentiment)

if __name__ == "__main__":
    spark = SparkSession.builder \
        .appName("RedditStreamProcessor") \
        .config("spark.jars.packages",
                "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.2,org.elasticsearch:elasticsearch-spark-30_2.12:8.7.0") \
        .getOrCreate()

    # Read streaming data from Kafka topic 'reddit_stream'.
    df = spark.readStream.format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "reddit_stream") \
        .load()

    # Convert the binary value from Kafka to string and parse the JSON.
    parsed_df = df.selectExpr("CAST(value AS STRING) as json_str") \
                  .select(from_json(col("json_str"), schema).alias("data")) \
                  .select("data.*")

    # Use the 'title' field for sentiment analysis
    processed_df = parsed_df.withColumn("sentiment", sentiment_udf(col("title")))

    # Convert 'created_utc' to a timestamp. Adjust this conversion if needed.
    processed_df = processed_df.withColumn("created_at", from_unixtime(col("created_utc").cast("long")).cast("timestamp"))

    # Aggregate sentiment over 1-minute windows.
    aggregated_df = processed_df.groupBy(window(col("created_at"), "1 minute")) \
                                .agg(avg("sentiment").alias("avg_sentiment"))

    # Write the aggregated results to the console for testing.
    query = processed_df.writeStream \
        .outputMode("append") \
        .format("org.elasticsearch.spark.sql") \
        .option("checkpointLocation", "/tmp/spark-checkpoints") \
        .option("es.nodes", "localhost") \
        .option("es.port", "9200") \
        .option("es.nodes.wan.only", "true") \
        .option("es.resource", "reddit_sentiment/_doc") \
        .start()

    query.awaitTermination()
