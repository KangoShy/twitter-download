import uuid
import tempfile
import os
import subprocess
import logging
import resource_operation as mine_minio
from sqlalchemy.orm import sessionmaker
from workflow.storage_operation import engine
from core.entity.mv_manage import MvManage
from core.vo.manage_param import InsertManage
from core.util.video import grab_frame


def execute(address: str, bucket_name: str, param: InsertManage):
    """ download to location """
    # location = download.x_download(address=address)
    location = "D:/mp4s/x1.mp4"
    if not os.path.exists(location) and not os.path.isfile(location):
        raise FileNotFoundError()

    if not location.lower().endswith('.mp4'):
        raise Exception(f'There is not a mp4 file, local path is {location}')

    identification = str(uuid.uuid1())
    temp_dir = tempfile.gettempdir().replace('\\', '/') + "/"
    """ 
    Push resources and home page images to minio. There are 3 types of files that need to be pushed
    1./temp_dir/identification.png
    2./temp_dir/identification.m3u8
    3./temp_dir/identification_segment_%d.ts ... 
    """
    match_prefix = temp_dir + identification
    home_picture = match_prefix + ".png"
    try:
        grab_frame(location, home_picture)
        mine_minio.upload_to_minio(file_temp_prefix=match_prefix, bucket_name=bucket_name)
        logging.info(f'Local file upload success, prefix is {match_prefix}!')
    except Exception as e:
        logging.error(f'Local file upload failed, message={e.message}')
        return

    """ convert mp4 to m3u8 and 6 seconds each """
    try:
        convert_mp4_to_m3u8(absolute_address=location, file_id=identification, output_address=temp_dir)
        logging.info(f'Local file convert to m3u8 already success, identification is {identification}!')
    except Exception as e:
        logging.error(f'Local file convert to m3u8 failed, message={e.message}')
        return

    """ inert to manage table """
    m3u8_file = bucket_name + '/' + identification + '.m3u8'
    home_picture = bucket_name + '/' + identification + '.png'
    insert_to_manage(m3u8_file=m3u8_file, home_picture=home_picture, param=param)
    logging.info('Local file record inert success!')


def convert_mp4_to_m3u8(absolute_address: str, file_id: str, output_address: str) -> None:
    """ only 5 seconds each """
    cmd = (f'ffmpeg -i {absolute_address} -c:v libx264 -c:a aac -hls_time 5 -hls_list_size 0 -hls_segment_filename '
           f'"{output_address}{file_id}_segment_%d.ts" '
           f'{output_address}{file_id}.m3u8')
    print('-----> ' + cmd)
    subprocess.call(cmd, shell=True)


def insert_to_manage(m3u8_file: str, home_picture: str, param: InsertManage):
    Session = sessionmaker(bind=engine)
    session = Session()
    manage = MvManage(blurb=param.blurb, picture=home_picture, address=m3u8_file, area=param.area,
                      class_tag=param.class_tag)
    session.add(manage)
    session.commit()
    session.close()


if __name__ == '__main__':
    execute(address='x', bucket_name='test', param=InsertManage(blurb='jianjie', area='台湾省', class_tag='标签'))
