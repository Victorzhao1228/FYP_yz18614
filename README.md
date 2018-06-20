# Speed Camera From Monocular View Using YOLO networks


## Introduction

Detecting speed of an approaching vehicle in a video sequence
Vehicle detection is implemented using YOLO v3
Speed calculation is implemented using a non-linear regression model
This Repository is modified from (https://github.com/qqwweee/keras-yolo3)

---

## Yolo network initiallisation

1. Download YOLOv3 weights from [YOLO website](http://pjreddie.com/darknet/yolo/).
2. Convert the Darknet YOLO model to a Keras model.

```
wget https://pjreddie.com/media/files/yolov3.weights
python convert.py yolov3.cfg yolov3.weights model_data/yolo.h5
```

---

## Usage

1. Setting input and output
In yolo_video.py, set the input video path and output path

2. Setting Region of Interest
In yolo.py
In function detect_image and detect_image_speed, set the variable box_range
This the area where user want to search for target vehicles

3. Change the speed calculation rate
In main
For example, if speed need to be calculated every 2 seconds,
then change Change
count % 30 == 0 to count % 60 == 0

4. To detect only an image,
Run yolo.py

5. Model_training folder includes Matlab Code to train the non-linear regression model

---

## Some issues to know

1. The test environment is
    - Python 3.6.3
    - Keras 2.1.5
    - Tensorflow 1.6.0

2. Default anchors are used.

3. The inference result is not totally the same as Darknet but the difference is small.

4. The speed is slower than Darknet. Replacing PIL with opencv may help a little.

5. Always load pretrained weights and freeze layers in the first stage of training. Or try Darknet training. It's OK if there is mismatch warning.


