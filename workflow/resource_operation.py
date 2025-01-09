import glob
import os

from minio.error import S3Error
from minio import Minio


def get_minio_client() -> Minio:
    return Minio(
        endpoint='101.55.67.178:9000', access_key='mQZ6UI4v8KYP7Be3ncij',
        secret_key='8QFk5SOWK8fhbRhu2UB6Pb3eZIS4gmTw8I3sQ5cu', secure=False  # Https will be 'True'
    )


def upload_to_minio(file_temp_prefix: str, bucket_name: str):
    client = get_minio_client()
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)
    """ match in prefix """
    file_paths = glob.glob(pathname=f'{file_temp_prefix}*', recursive=False, include_hidden=False)
    for file_path in file_paths:
        object_name = os.path.basename(file_path)
        try:
            client.fput_object(bucket_name, object_name, file_path)
            print(f'Successfully uploaded {object_name}')
        except S3Error as e:
            print(f'Upload failure {object_name}, message={e.message}')
