import uuid
import tempfile
import download
import os
import subprocess
import logging


def execute(address: str):
    # download to location
    location = download.x_download(address=address)
    if not os.path.exists(location) and not os.path.isfile(location):
        raise FileNotFoundError()

    if not location.lower().endswith('.mp4'):
        raise Exception(f'There is not a mp4 file, local path is {location}')
    # convert mp4 to m3u8 and 6 seconds each
    identification = str(uuid.uuid1())
    temp_dir = tempfile.gettempdir()
    convert_mp4_to_m3u8(absolute_address=location, file_id=identification, output_address=temp_dir)
    logging.info('')


def convert_mp4_to_m3u8(absolute_address: str, file_id: str, output_address: str) -> None:
    cmd = (f'ffmpeg -i {absolute_address} -c:v libx264 -c:a aac -hls_time 5 -hls_list_size 0 -hls_segment_filename '
           f'"{output_address}{file_id}_segment_%d.ts" '
           f'{output_address}{file_id}.m3u8')
    subprocess.call(cmd, shell=True)
