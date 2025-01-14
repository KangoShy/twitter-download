import uuid
import tempfile
import os
import subprocess
import logging
from databases import minio as mine_minio
from sqlalchemy.orm import sessionmaker
from databases.mysql import engine
from core.entity.mv_manage import MvManage
from core.vo.manage_param import InsertManage
from core.util.video import grab_frame
import shutil
from pathlib import Path


def execute(address: str, bucket_name: str, param: InsertManage) -> dict:
    """ download to location """
    # local_path = download.x_download(address=address)
    local_path = "D:/mp4s/x1.mp4"
    if not os.path.exists(local_path) and not os.path.isfile(local_path):
        raise FileNotFoundError()

    if not local_path.lower().endswith('.mp4'):
        raise Exception(f'There is not a mp4 file, local path is {local_path}')

    identification = str(uuid.uuid1())
    temp_dir = create_folder_return_path(tempfile.gettempdir().replace('\\', '/') + "/" + identification + "/")

    match_prefix = temp_dir + identification
    home_picture = create_file_return_path(match_prefix + ".png")

    """ convert mp4 to m3u8 and 6 seconds each """
    try:
        convert_mp4_to_m3u8(absolute_address=local_path, file_id=identification, output_address=temp_dir)
        logging.info(f'Local file convert to m3u8 already success, identification is {identification}')
    except Exception as e:
        logging.error(f'Local file convert to m3u8 failed, message={e.message}')
        return {}

    """ 
    Push resources and home page images to minio. There are 3 types of files that need to be pushed
    1./temp_dir/identification.png
    2./temp_dir/identification.m3u8
    3./temp_dir/identification_segment_%d.ts ... 
    """
    try:
        grab_frame(local_path, home_picture)
        mine_minio.upload_to_minio(file_temp_prefix=match_prefix, bucket_name=bucket_name)
        logging.info(f'Local file upload success, prefix is {match_prefix}')
    except Exception as e:
        logging.error(f'Local file upload failed, message={e.message}')
        return {}
    finally:
        shutil.rmtree(path=temp_dir, ignore_errors=True, onerror=None)

    """ inert to manage table """
    m3u8_file = bucket_name + '/' + identification + '.m3u8'
    home_picture = bucket_name + '/' + identification + '.png'
    insert_to_manage(m3u8_file=m3u8_file, home_picture=home_picture, param=param)
    logging.info('Local file record inert success')
    return {
        "m3u8_path": m3u8_file,
        "home_picture": home_picture
    }


def convert_mp4_to_m3u8(absolute_address: str, file_id: str, output_address: str) -> None:
    """ only 5 seconds each """
    cmd = (f'ffmpeg -i {absolute_address} -c:v libx264 -c:a aac -hls_time 5 -hls_list_size 0 -hls_segment_filename '
           f'"{output_address}{file_id}_segment_%d.ts" '
           f'{output_address}{file_id}.m3u8')
    print('-----> ' + cmd)
    subprocess.call(cmd, shell=True)


def create_folder_return_path(path: str) -> str:
    _path = Path(path)
    _path.mkdir()
    return path


def create_file_return_path(path: str) -> str:
    _file = Path(path)
    _file.touch()
    return path


def insert_to_manage(m3u8_file: str, home_picture: str, param: InsertManage):
    Session = sessionmaker(bind=engine)
    session = Session()
    manage = MvManage(blurb=param.blurb, picture=home_picture, address=m3u8_file, area=param.area,
                      class_tag=param.class_tag)
    session.add(manage)
    session.commit()
    session.close()
