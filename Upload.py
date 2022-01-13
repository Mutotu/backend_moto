import boto3
import os


session = boto3.session.Session()
client = session.client("s3", region_name="USWest", aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"), aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"))

def upload_image(url):
    client.upload_file(url, "file.ext")
