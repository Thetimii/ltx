import boto3
import os
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

def get_s3_client():
    return boto3.client(
        's3',
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
        region_name=os.environ.get('AWS_REGION', 'us-east-1')
    )

def upload_file_to_s3(file_name, bucket, object_name=None, expiration=3600*24):
    """Upload a file to an S3 bucket and return a presigned URL."""

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = get_s3_client()
    try:
        s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logger.error(e)
        return None

    # Generate presigned URL
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logger.error(e)
        return None

    # If the user wants a clean public URL and their bucket is configured for it,
    # they can skip using the query params, but returning the presigned URL is safest.
    return response

if __name__ == "__main__":
    # Test stub
    pass
