import cv2
import matplotlib.pyplot as plt
import numpy as np
from tkinter import filedialog
import cvzone


def glasses_filter(image):
    """
    adds glasses to the given image face
    """
    img = plt.imread(image)
    img_copy = img.copy()

    eye_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    eye = eye_cascade.detectMultiScale(img)[0]
    eye_x, eye_y, eye_w, eye_h = eye

    # read the glasses image and resiz it to fit the face
    # coordinates
    glasses = cv2.imread("images/glass.png", cv2.IMREAD_UNCHANGED)
    glasses_resize = cv2.resize(glasses, (eye_w + 50, eye_h + 55))

    frame = cvzone.overlayPNG(img, glasses_resize, [eye_x - 45, eye_y - 75])

    cv2.imshow(frame)

    # replace the pixels of the image of Hermione
    # with the pixels of the glasses.
    # for i in range(glasses.shape[0]):
    #     for j in range(glasses.shape[1]):
    #         if glasses[i, j, 3] > 0:
    #             img_copy[eye_y + i - 20, eye_x + j - 23, :] = glasses[
    #                 i, j, :-1
    #             ]

    return img_copy
