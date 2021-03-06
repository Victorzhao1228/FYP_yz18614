#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Run a YOLO_v3 style detection model on test images.
"""

import colorsys
import os
from timeit import default_timer as timer
from moviepy.editor import VideoFileClip
import numpy as np
from keras import backend as K
from keras.models import load_model
from keras.layers import Input
from PIL import Image, ImageFont, ImageDraw
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2
import math
import time


from yolo3.model import yolo_eval, yolo_body, tiny_yolo_body
from yolo3.utils import letterbox_image


class YOLO(object):
    def __init__(self):
        self.model_path = 'model_data/yolo.h5' # model path or trained weights path
        self.anchors_path = 'model_data/yolo_anchors.txt'
        self.classes_path = 'model_data/coco_classes.txt'
        self.score = 0.4
        self.iou = 0.45
        self.class_names = self._get_class()
        self.anchors = self._get_anchors()
        self.sess = K.get_session()
        self.model_image_size = (416, 416) # fixed size or (None, None), hw
        self.boxes, self.scores, self.classes = self.generate()

    def _get_class(self):
        classes_path = os.path.expanduser(self.classes_path)
        with open(classes_path) as f:
            class_names = f.readlines()
        class_names = [c.strip() for c in class_names]
        return class_names

    def _get_anchors(self):
        anchors_path = os.path.expanduser(self.anchors_path)
        with open(anchors_path) as f:
            anchors = f.readline()
        anchors = [float(x) for x in anchors.split(',')]
        return np.array(anchors).reshape(-1, 2)

    def generate(self):
        model_path = os.path.expanduser(self.model_path)
        assert model_path.endswith('.h5'), 'Keras model or weights must be a .h5 file.'

        # Load model, or construct model and load weights.
        num_anchors = len(self.anchors)
        num_classes = len(self.class_names)
        is_tiny_version = num_anchors==6 # default setting
        try:
            self.yolo_model = load_model(model_path, compile=False)
        except:
            self.yolo_model = tiny_yolo_body(Input(shape=(None,None,3)), num_anchors//2, num_classes) \
                if is_tiny_version else yolo_body(Input(shape=(None,None,3)), num_anchors//3, num_classes)
            self.yolo_model.load_weights(self.model_path) # make sure model, anchors and classes match
        else:
            assert self.yolo_model.layers[-1].output_shape[-1] == \
                num_anchors/len(self.yolo_model.output) * (num_classes + 5), \
                'Mismatch between model and given anchor and class sizes'

        print('{} model, anchors, and classes loaded.'.format(model_path))

        # Generate colors for drawing bounding boxes.
        hsv_tuples = [(x / len(self.class_names), 1., 1.)
                      for x in range(len(self.class_names))]
        self.colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
        self.colors = list(
            map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)),
                self.colors))
        np.random.seed(10101)  # Fixed seed for consistent colors across runs.
        np.random.shuffle(self.colors)  # Shuffle colors to decorrelate adjacent classes.
        np.random.seed(None)  # Reset seed to default.

        # Generate output tensor targets for filtered bounding boxes.
        self.input_image_shape = K.placeholder(shape=(2, ))
        boxes, scores, classes = yolo_eval(self.yolo_model.output, self.anchors,
                len(self.class_names), self.input_image_shape,
                score_threshold=self.score, iou_threshold=self.iou)
        return boxes, scores, classes

    def detect_image(self, image):
        distance_now = 0
        start = timer()
        box_range = [0, 0, 480 , 360]
        croped_img = image.crop((box_range[0], box_range[1], box_range[2], box_range[3]))
        #croped_img = image

        if self.model_image_size != (None, None):
            assert self.model_image_size[0]%32 == 0, 'Multiples of 32 required'
            assert self.model_image_size[1]%32 == 0, 'Multiples of 32 required'
            boxed_image = letterbox_image(croped_img, tuple(reversed(self.model_image_size)))
        else:
            new_image_size = (croped_img.width - (croped_img.width % 32),
                              croped_img.height - (croped_img.height % 32))
            boxed_image = letterbox_image(croped_img, new_image_size)
        image_data = np.array(boxed_image, dtype='float32')

        image_data /= 255.
        image_data = np.expand_dims(image_data, 0)  # Add batch dimension.

        out_boxes, out_scores, out_classes = self.sess.run(
            [self.boxes, self.scores, self.classes],
            feed_dict={
                self.yolo_model.input: image_data,
                self.input_image_shape: [croped_img.size[1], croped_img.size[0]],
                K.learning_phase(): 0
            })

        font = ImageFont.truetype(font='font/FiraMono-Medium.otf',
                    size=np.floor(3e-2 * image.size[1] + 0.5).astype('int32'))
        thickness = (croped_img.size[0] + croped_img.size[1]) // 300

        for i, c in reversed(list(enumerate(out_classes))):
            predicted_class = self.class_names[c]
            box = out_boxes[i]
            score = out_scores[i]

            if predicted_class == 'car':
                label = '{} {:.2f}'.format(predicted_class, score)
                draw = ImageDraw.Draw(image)
                label_size = draw.textsize(label, font)

                top, left, bottom, right = box
                top = max(0, np.floor(top + 0.5).astype('int32')) #+ box_range[1]
                left = max(0, np.floor(left + 0.5).astype('int32')) #+ box_range[0]
                bottom = min(image.size[1], np.floor(bottom + 0.5).astype('int32')) #+ box_range[1]
                right = min(image.size[0], np.floor(right + 0.5).astype('int32')) #+ box_range[0]
                print(label, (left, top), (right, bottom))

                width = right - left
                distance_now = 273.5121 * math.exp(-0.0573 * width) + 39.08 * math.exp(-0.0067 * width)
                # print(distance_now)

                d = "{0:.2f}".format(distance_now)
                text = str(d) + 'm'

                if top - label_size[1] >= 0:
                    text_origin = np.array([left, top - label_size[1]])
                else:
                    text_origin = np.array([left, top + 1])

                if top - label_size[1] >= 0:
                    distance_origin = np.array([left, top + label_size[1]])
                else:
                    distance_origin = np.array([left, top + 1])

            # My kingdom for a good redistributable image drawing library.
                for i in range(thickness):
                    draw.rectangle(
                        [left + i, top + i, right - i, bottom - i],
                        outline=self.colors[c])
                draw.rectangle(
                    [tuple(text_origin), tuple(text_origin + label_size)],
                    fill=self.colors[c])
                draw.text(text_origin, label, fill=(0, 0, 0), font=font)


                draw.rectangle(
                    [tuple(distance_origin), tuple(distance_origin + label_size)],
                    fill=self.colors[c])
                draw.text(distance_origin, d, fill=(0, 0, 0), font=font)
                del draw


        end = timer()
        print(end - start)
        return image

    def detect_image_speed(self, image):
        distance_now = 0
        start = timer()
        box_range = [0, 0, 480, 360]
        croped_img = image.crop((box_range[0], box_range[1], box_range[2], box_range[3]))
        #croped_img = image

        if self.model_image_size != (None, None):
            assert self.model_image_size[0]%32 == 0, 'Multiples of 32 required'
            assert self.model_image_size[1]%32 == 0, 'Multiples of 32 required'
            boxed_image = letterbox_image(croped_img, tuple(reversed(self.model_image_size)))
        else:
            new_image_size = (croped_img.width - (croped_img.width % 32),
                              croped_img.height - (croped_img.height % 32))
            boxed_image = letterbox_image(croped_img, new_image_size)
        image_data = np.array(boxed_image, dtype='float32')

        image_data /= 255.
        image_data = np.expand_dims(image_data, 0)  # Add batch dimension.

        out_boxes, out_scores, out_classes = self.sess.run(
            [self.boxes, self.scores, self.classes],
            feed_dict={
                self.yolo_model.input: image_data,
                self.input_image_shape: [croped_img.size[1], croped_img.size[0]],
                K.learning_phase(): 0
            })

        font = ImageFont.truetype(font='font/FiraMono-Medium.otf',
                    size=np.floor(3e-2 * image.size[1] + 0.5).astype('int32'))
        thickness = (croped_img.size[0] + croped_img.size[1]) // 300

        for i, c in reversed(list(enumerate(out_classes))):
            predicted_class = self.class_names[c]
            box = out_boxes[i]
            score = out_scores[i]

            if predicted_class == 'car':
                label = '{} {:.2f}'.format(predicted_class, score)
                draw = ImageDraw.Draw(image)
                label_size = draw.textsize(label, font)

                top, left, bottom, right = box
                top = max(0, np.floor(top + 0.5).astype('int32')) #+ box_range[1]
                left = max(0, np.floor(left + 0.5).astype('int32')) #+ box_range[0]
                bottom = min(image.size[1], np.floor(bottom + 0.5).astype('int32')) #+ box_range[1]
                right = min(image.size[0], np.floor(right + 0.5).astype('int32')) #+ box_range[0]
                print(label, (left, top), (right, bottom))

                width = right - left
                distance_now = 273.5121 * math.exp(-0.0573 * width) + 39.08 * math.exp(-0.0067 * width)
                # print(distance_now)
                d = "{0:.2f}".format(distance_now)
                text = str(d) + 'm'

                if top - label_size[1] >= 0:
                    text_origin = np.array([left, top - label_size[1]])
                else:
                    text_origin = np.array([left, top + 1])

                if top - label_size[1] >= 0:
                    distance_origin = np.array([left, top + label_size[1]])
                else:
                    distance_origin = np.array([left, top + 1])

            # My kingdom for a good redistributable image drawing library.
                for i in range(thickness):

                    draw.rectangle(
                        [left + i, top + i, right - i, bottom - i],
                        outline=self.colors[c])
                draw.rectangle(
                    [tuple(text_origin), tuple(text_origin + label_size)],
                    fill=self.colors[c])
                draw.text(text_origin, label, fill=(0, 0, 0), font=font)


                draw.rectangle(
                    [tuple(distance_origin), tuple(distance_origin + label_size)],
                    fill=self.colors[c])
                draw.text(distance_origin, d, fill=(0, 0, 0), font=font)
                del draw


        end = timer()
        print(end - start)
        return distance_now,image


    def close_session(self):
        self.sess.close()


def detect_video(yolo, video_path, output_path=""):
    import cv2
    distance_past = 0
    vid = cv2.VideoCapture(video_path)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, 30.0, (480, 360))
    speed = "Speed: ??"
    prev_time = timer()


    while (vid.isOpened()):
        count = 1;

        ret, frame = vid.read()
        image = Image.fromarray(frame)
        distance_now, image = yolo.detect_image_speed(image)
        result = np.asarray(image)

        v = abs(distance_past - distance_now) / 1 * 3.6
        v = "{0:.2f}".format(v)
        print(v)
        speed = "Speed:" + str(v) + "km/h"

        cv2.putText(result, text=speed, org=(15, 100), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.50, color=(255, 255, 255), thickness=2)
        distance_past = distance_now
        if ret == True:
            out.write(result)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

        while count <= 30:
            ret, frame = vid.read()
            image = Image.fromarray(frame)
            image = yolo.detect_image(image)
            result = np.asarray(image)
            cv2.putText(result, text=speed, org=(15, 100), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=0.50, color=(255, 255, 255), thickness=2)
            if ret == True:
                out.write(frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break
            count = count + 1


    yolo.close_session()
    vid.release()
    out.release()
    cv2.destroyAllWindows()


def detect_img(yolo):
    #filename = '/Users/Victor/Desktop/dis/distance/70_small.jpg'

    #image = Image.open(filename)
    #r_image = yolo.detect_image(image)
    #r_image.show()
    #yolo.close_session()

    while True:
        img = input('Input image filename:')
        try:
            image = Image.open(img)
        except:
            print('Open Error! Try again!')
            continue
        else:
            distance_now, r_image = yolo.detect_image(image)
            r_image.show()
    yolo.close_session()


if __name__ == '__main__':
    detect_img(YOLO())
