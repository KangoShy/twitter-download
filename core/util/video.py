from moviepy import VideoFileClip
from PIL import Image


def grab_frame(video_file_path, output_image_path):
    try:
        """ Frame at 5 seconds """
        clip = VideoFileClip(video_file_path)
        frame = clip.get_frame(5)
        image = Image.fromarray(frame)
        target_width, target_height = 1280, 720
        scale = max(target_width / image.width, target_height / image.height)
        scaled_size = (int(image.width * scale), int(image.height * scale))
        scaled_image = image.resize(scaled_size, Image.Resampling.LANCZOS)
        """ Crop the image to the specified size """
        x = (scaled_image.width - target_width) // 2
        y = (scaled_image.height - target_height) // 2
        cropped_image = scaled_image.crop((x, y, x + target_width, y + target_height))
        cropped_image.save(output_image_path, "PNG")
        clip.close()

    except Exception as e:
        print(f"获取视频截图并裁剪失败: {e}")


if __name__ == '__main__':
    grab_frame("D:/mp4s/x1.mp4", "D:/mp4s/x1.png")
