# Twitter Streaming Pipeline

A real-time data pipeline for streaming and processing Twitter data. This project demonstrates how to ingest, process, and visualize Twitter data using a combination of tools such as Apache Kafka, Apache Spark, and Elasticsearch with Kibana.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Setup](#setup)
- [Usage](#usage)
- [Commit Message Guidelines](#commit-message-guidelines)
- [Contributing](#contributing)
- [License](#license)

## Overview

The **Twitter Streaming Pipeline** project simulates a real-time data processing scenario where tweets are ingested via Twitter's API, streamed through Apache Kafka, processed using Apache Spark (or Apache Flink), and stored in Elasticsearch for visualization in Kibana. This pipeline serves as a reference for building scalable data architectures and is a portfolio project demonstrating industry-standard practices.

## Features

- **Real-time Tweet Ingestion:** Capture live tweets based on specific keywords or hashtags.
- **Stream Processing:** Process and analyze tweet data in real time.
- **Data Visualization:** Store processed data in Elasticsearch and create dashboards in Kibana.
- **Modular Design:** Separate components for data ingestion, processing, and visualization.

## Project Structure

```plaintext
twitter-streaming-pipeline/
├── producer/            # Twitter producer scripts
│   ├── __init__.py
│   └── twitter_producer.py
├── streaming/           # Spark streaming or processing code
│   ├── __init__.py
│   └── spark_processor.py
├── visualization/       # Configurations/scripts for Elasticsearch/Kibana
│   └── docker-compose.yml
├── docs/                # Documentation, architecture diagrams, etc.
│   └── architecture.md
├── tests/               # Unit and integration tests
│   └── test_sample.py
├── .gitignore           # Git ignore file (includes .venv/, __pycache__/, *.pyc, etc.)
├── README.md            # This file
└── requirements.txt     # Project dependencies
```

## Setup

### Clone the Repository
```bash
git clone git@github-tech:yourusername/twitter-streaming-pipeline.git
cd twitter-streaming-pipeline
```

### Set Up a Virtual Environment:

```bash
Copy
python3 -m venv .venv
source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
```

### Install Dependencies:

```bash
Copy
pip install -r requirements.txt
```

### Configure Environment Variables:

Create a .env file in the root directory to store sensitive information (e.g., Twitter API keys). An example entry might be:

```plaintext
TWITTER_CONSUMER_KEY=your_consumer_key
TWITTER_CONSUMER_SECRET=your_consumer_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
```

### Set Up Docker/Orbstack Environment (if applicable):

Use the provided docker-compose.yml in the visualization/ folder to start Kafka, Elasticsearch, and Kibana:

```bash
docker-compose -f visualization/docker-compose.yml up -d
```

## Usage

### Start the Twitter Producer:
Run the producer script to begin streaming tweets:

```bash
python producer/twitter_producer.py
```

### Start the Streaming Processor:

Run the Spark streaming job (adjust the command as needed for your Spark setup):

```bash
python streaming/spark_processor.py
```
### View Data:

Access Kibana at http://localhost:5601 to visualize the processed tweet data.

## Commit Message Guidelines
We follow the Conventional Commits standard to maintain a clear and consistent commit history. Below are some quick guidelines:

### Commit Types:

- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `chore:` for routine tasks (e.g., configuration updates, refactoring)
- `style:` for formatting changes
- `refactor:` for code restructuring without changing behavior

### Format:

`<type>: <short summary>`

`<detailed explanation>`

## Example:
chore: update .gitignore to exclude .venv directory

Add .venv/ to .gitignore to prevent tracking of the virtual environment.

## Contributing
Contributions are welcome! 

### Please follow these steps:

- Fork the repository.
- Create a new branch (git checkout -b feature/your-feature).
- Make your changes and commit them following the commit message guidelines.
- Push to your branch and open a pull request.