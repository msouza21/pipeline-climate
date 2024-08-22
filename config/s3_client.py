import os, boto3, json
from dotenv import load_dotenv
load_dotenv()


config_path = os.path.join("../../ignore/config.json")

s3_bucket = 's3bucketsz'
s3_prefix = 'data/'

with open(config_path) as file:
    data = json.load(file)
    aws_creds = data["AWS"]

def create_client():
    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    region_name = os.getenv("AWS_REGION_NAME")

    s3 = boto3.client(
        's3',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=region_name
    )
    
    return s3

s3_client = create_client()