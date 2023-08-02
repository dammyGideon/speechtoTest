import boto3 
import os

def Config():
    aws_region = os.getenv('AWS_REGION')
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

    polly_client = boto3.client('polly', region_name=aws_region,
                                aws_access_key_id=aws_access_key_id,
                                aws_secret_access_key=aws_secret_access_key)
    
    return polly_client
