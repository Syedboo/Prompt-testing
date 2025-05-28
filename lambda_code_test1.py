import json
import boto3
from datetime import datetime
from transformers import pipeline, logging

# Initialize S3 client
s3_client = boto3.client('s3')

# Suppress warnings from Hugging Face transformers library
logging.set_verbosity_error()

# Explicitly initialize the sentiment analysis pipeline with a specific model
sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")


def lambda_handler(event, context):
    try:
        # Define the S3 bucket and file locations
        bucket_name = 'stockmarketprodata'
        input_key = 'Newsdata/raw/articles_data_SBRY.L.json'  # Input file path in S3
        output_key = 'Newsdata/processed/processed_articles_data_SBRY.L.json'  # Output file path in S3

        # Download the JSON file from S3
        response = s3_client.get_object(Bucket=bucket_name, Key=input_key)
        articles_data = response['Body'].read().decode('utf-8')
        articles = json.loads(articles_data)

        # Process articles to extract and convert dates
        for article in articles:
            if "date" in article and article["date"]:
                # Convert the date into a datetime object
                date_time = datetime.strptime(article["date"], "%a, %d %b %Y %H:%M:%S GMT")
                article["actual_date"] = date_time.date().isoformat()
                article["time"] = date_time.time().strftime("%H:%M:%S")

                # Truncate the text to the maximum length allowed by the model
                text = article["text"][:512]

                # Get sentiment analysis results
                sentiment_result = sentiment_pipeline(text)[0]

                # Convert the sentiment label to a score between 0 and 1
                sentiment_label = sentiment_result['label']
                sentiment_score = sentiment_result['score']
                if sentiment_label == "NEGATIVE":
                    sentiment_score = 1 - sentiment_score  # Invert score for negative sentiment

                # Assign sentiment score to the article
                article["sentiment_score"] = sentiment_score
                article["insights"] = sentiment_result['label']
            else:
                article["actual_date"] = None
                article["time"] = None
                article["sentiment_score"] = None
                article["insights"] = None

        # Convert the processed articles back to JSON
        processed_articles_data = json.dumps(articles, indent=4)

        # Upload the processed JSON back to S3
        s3_client.put_object(Bucket=bucket_name, Key=output_key, Body=processed_articles_data)

        return {
            'statusCode': 200,
            'body': json.dumps('Articles processed and saved successfully!')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error processing articles: {str(e)}')
        }
