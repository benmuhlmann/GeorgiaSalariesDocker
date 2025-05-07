import boto3
import os
import pandas as pd
import io
from dotenv import load_dotenv

def initialize_s3_client():
    """Initialize and return an S3 client with credentials from environment variables."""
    load_dotenv()
    return boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION', 'us-east-1')
    )

def load_data_from_s3(s3_client):
    """
    Load the salary dataset from S3.
    
    Args:
        s3_client: Initialized boto3 S3 client
        
    Returns:
        pandas.DataFrame: The loaded dataset or None if loading fails
    """
    try:
        print("Attempting to fetch data from S3...")
        response = s3_client.get_object(
            Bucket=os.getenv('S3_BUCKET_NAME'),
            Key='all_salaries.parquet'
        )
        data = pd.read_parquet(io.BytesIO(response['Body'].read()))
        print("Dataset loaded successfully from S3.")
        return data
    except Exception as e:
        print(f"Error loading data from S3: {e}")
        return None 