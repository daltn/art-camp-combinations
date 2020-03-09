import boto3
from botocore.exceptions import ClientError
import logging


def upload_file(file_name, bucket, object_name=None):
    if object_name is None:
        object_name = file_name

    session = boto3.Session(profile_name='artcamp')
    s3_client = session.client('s3')

    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def list_files(bucket):
    s3 = boto3.client('s3')
    contents = []
    try:
        for item in s3.list_objects(Bucket=bucket)['Contents']:
            print(item)
            contents.append(item)
    except Exception as e:
        pass

    return contents
