import os
import json
import praw
from kafka import KafkaProducer
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Initialize the Reddit client
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

# Set up the Kafka producer; adjust bootstrap_servers if needed
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Select the subreddit you want to stream (e.g., "news")
subreddit = reddit.subreddit("news")

print("Starting to stream submissions from r/news...")

# Stream new submissions continuously
for submission in subreddit.stream.submissions():
    data = {
        "id": submission.id,
        "title": submission.title,
        "selftext": submission.selftext,
        "created_utc": submission.created_utc,
        "url": submission.url,
        "author": str(submission.author)
    }
    # Send the submission data to the 'reddit_stream' Kafka topic
    producer.send('reddit_stream', data)
    print("Sent submission:", data)
