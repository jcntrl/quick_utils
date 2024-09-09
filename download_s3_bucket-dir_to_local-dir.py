import boto3
import os


def download_s3_bucket_to_directory(region:str, s3_bucket:str, s3_directory:str, dest_directory) -> None:

    # Initialize S3 client
    s3 = boto3.client(
        's3',
        # aws_access_key_id='AWS_ACCESS_KEY_ID',
        # aws_secret_access_key='AWS_SECRET_ACCESS_KEY',
        region_name=region
    )

    bucket_name = s3_bucket
    s3_directory = s3_directory
    
    # Create a local directory if it doesn't exist
    local_directory = dest_directory
    if not os.path.exists(local_directory):
        os.makedirs(local_directory)

    # List all objects in the S3 directory
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=s3_directory)

    # Download each file from the directory
    if 'Contents' in response:
        for obj in response['Contents']:
            file_key = obj['Key']

            # Remove the S3 directory from the file_key to avoid nested directories
            relative_path = file_key[len(s3_directory):].lstrip('/')

            # Create the full local file path
            local_file_path = os.path.join(local_directory, relative_path)

            # If the object is a file (not a directory), create necessary directories and download it
            local_file_dir = os.path.dirname(local_file_path)
            if not os.path.exists(local_file_dir):
                os.makedirs(local_file_dir)

            # Skip creating directories for files that start with '.' (hidden files)
            if not file_key.endswith('/'):
                # Download the file
                s3.download_file(bucket_name, file_key, local_file_path)
                print(f"Downloaded {file_key} to {local_file_path}")
    else:
        print(f"No files found in directory: {s3_directory}")