import subprocess


# client = Minio(endpoint='103.178.57.34:9000', access_key='Qw3fq14h5wD1kNVYvXnq',
#                secret_key='IOtgeoZwlmgSYamrNviaTnrndvrPEKf91onYXsIJ', secure=False  # 如果是 HTTPS 连接，则设置为 True
#                )
# bucket_name = 'video'
#
# if not client.bucket_exists(bucket_name):
#     client.make_bucket(bucket_name)


# twitter下载的mp4转为m3u8
def convert_mp4_to_m3u8():
    cmd = (f'ffmpeg -i {input_file} -c:v libx264 -c:a aac -hls_time 10 -hls_list_size 0 -hls_segment_filename '
           f'"/Users/kangoshayne/Downloads/工作下载目录/学习资料/segment_%d.ts" {output_file}')
    subprocess.call(cmd, shell=True)


# 指定输入的MP4文件和输出的M3U8文件路径
input_file = '/Users/kangoshayne/Downloads/工作下载目录/学习资料/20.mp4'
output_file = '/Users/kangoshayne/Downloads/工作下载目录/学习资料/20.m3u8'





















if __name__ == '__main__':
    convert_mp4_to_m3u8()
