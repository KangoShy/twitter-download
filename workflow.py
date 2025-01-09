import subprocess
import uuid
import glob
from configparser import Error
import pathlib
from workflow.resource_operation import Minio
import os
from workflow.resource_operation import S3Error

twitter_mp4_file_path = '/Users/kangoshayne/Downloads/x/'
mp4_to_m3u8_output_path = '/Users/kangoshayne/Downloads/m3u8/'
bucket_name = 'xxxx'


# The interval value is the file name, and the mp4 files in the interval are converted to m3u8
# format in batches
def read_by_serial_number(range_p: str):
    start, end = range_p.split('-', 1)
    for number in range(int(start), int(end) + 1):

        # The file absolute address
        absolute_address = f'{twitter_mp4_file_path}{number}.mp4'
        if not file_exists(absolute_address):
            print(f'No found of the file named {number}...')
            continue
        file_temp_prefix = str(uuid.uuid4())
        try:
            convert_mp4_to_m3u8(absolute_address, file_temp_prefix)
        except Error as e:
            print(f'The file named {number} failed to be converted，message={e.message}')

        # Upload to minio storage
        upload_to_minio(file_temp_prefix)


# Used fput function
def upload_to_minio(file_temp_prefix: str):
    check_bucket_exists()
    client = get_minio_client()
    file_paths = glob.glob(pathname=f'{mp4_to_m3u8_output_path}{file_temp_prefix}*',
                           recursive=False,
                           include_hidden=False
                           )
    for file_path in file_paths:
        object_name = os.path.basename(file_path)
        try:
            client.fput_object(bucket_name, object_name, file_path)
            print(f'Successfully uploaded {object_name}')
        except S3Error as e:
            print(f'Upload failure {object_name}, message={e.message}')


# Twitter downloads mp4 to m3u8
def convert_mp4_to_m3u8(absolute_address: str, file_temp_prefix: str) -> None:
    cmd = (f'ffmpeg -i {absolute_address} -c:v libx264 -c:a aac -hls_time 5 -hls_list_size 0 -hls_segment_filename '
           f'"{mp4_to_m3u8_output_path}{file_temp_prefix}_segment_%d.ts" '
           f'{mp4_to_m3u8_output_path}{file_temp_prefix}.m3u8')
    subprocess.call(cmd, shell=True)


# File check
def file_exists(filepath: str):
    path = pathlib.Path(filepath)
    return path.exists() and path.is_file()


# Check bucket
def check_bucket_exists():
    client = get_minio_client()
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)


# Get a minio client
def get_minio_client() -> Minio:
    return Minio(endpoint='103.178.57.34:8999',
                 access_key='Qw3fq14h5wD1kNVYvXnq',
                 secret_key='IOtgeoZwlmgSYamrNviaTnrndvrPEKf91onYXsIJ',
                 secure=False  # Https will be 'True'
                 )


if __name__ == '__main__':
    read_by_serial_number('1-19')
