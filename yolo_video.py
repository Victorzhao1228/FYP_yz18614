import sys
from yolo import YOLO
from yolo import detect_video

if __name__ == '__main__':
    video_path = '/Users/Victor/Desktop/test2.mp4'
    output_path = '/Users/Victor/Desktop/haha.mp4'
    detect_video(YOLO(), video_path, output_path)
