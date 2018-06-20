import colorsys
import os
from timeit import default_timer as timer
from moviepy.editor import VideoFileClip
import numpy as np
from PIL import Image, ImageFont, ImageDraw
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2
import math
import time

if __name__ == "__main__":
     # YOLO Pipeline

     video_path = '/Users/Victor/Desktop/3.m4v'
     output_path = '/Users/Victor/Desktop/haha.mp4'
     final = '/Users/Victor/Desktop/final.mp4'


     cap = VideoFileClip(video_path)
     cap = cap.set_fps(10.0)
     cap.write_videofile(output_path, audio=False)

     vid = cv2.VideoCapture(output_path)

     fourcc = cv2.VideoWriter_fourcc(*'XVID')
     out = cv2.VideoWriter(final, fourcc, 10.0, (1280, 720))

     while (vid.isOpened()):
        ret, frame = vid.read()
        if ret == True:

            out.write(frame)
            cv2.imshow('frame', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

vid.release()
out.release()
cv2.destroyAllWindows()
