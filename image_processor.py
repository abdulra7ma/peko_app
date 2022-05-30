import cv2
import cvzone
import matplotlib.pyplot as plt
from PIL import Image
from PIL.ExifTags import TAGS

from helpers import convert_from_cv2_to_image, convert_from_image_to_cv2


def image_overlay_second_method(
    img1, img2, location, min_thresh=0, is_transparent=False
):
    h, w = img1.shape[:2]
    h1, w1 = img2.shape[:2]
    x, y = location
    roi = img1[y : y + h1, x : x + w1]

    gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, min_thresh, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)

    img_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
    img_fg = cv2.bitwise_and(img2, img2, mask=mask)
    dst = cv2.add(img_bg, img_fg)
    if is_transparent:
        dst = cv2.addWeighted(
            img1[y : y + h1, x : x + w1], 0.1, dst, 0.9, None
        )
    img1[y : y + h1, x : x + w1] = dst
    return img1


def glasses_filter(image):
    """
    adds glasses to the given image face
    """
    img = convert_from_image_to_cv2(image)
    img_copy = img.copy()

    eye_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    eye = eye_cascade.detectMultiScale(img)[0]
    eye_x, eye_y, eye_w, eye_h = eye

    # read the glasses image and resiz it to fit the face
    # coordinates
    glasses = cv2.imread("images/glass.png", cv2.IMREAD_UNCHANGED)
    glasses_resize = cv2.resize(glasses, (eye_w + 50, eye_h + 55))

    # cv2.imshow(glasses_resize)

    # filtered_img = image_overlay_second_method(
    #     img_copy, glasses_resize, (eye_x - 45, eye_y - 75)
    # )

    try:
        frame = cvzone.overlayPNG(
            img, glasses_resize, [eye_x - 45, eye_y - 75]
        )
    except ValueError:
        frame = cvzone.overlayPNG(
            img, glasses_resize, [eye_x - 10, eye_y - 10]
        )

    # cv2.imshow(frame)

    # replace the pixels of the image of Hermione
    # with the pixels of the glasses.
    # for i in range(glasses.shape[0]):
    #     for j in range(glasses.shape[1]):
    #         if glasses[i, j, 3] > 0:
    #             img_copy[eye_y + i - 20, eye_x + j - 23, :] = glasses[
    #                 i, j, :-1
    #             ]

    return convert_from_cv2_to_image(frame)


def black_and_white(image: Image):
    """
    Converts an image into a black and white
    """

    og_img = cv2.imread(image.filename)
    wb_img = cv2.cvtColor(og_img, cv2.COLOR_BGR2GRAY)

    ## save the newly created image locally
    # image_name = str(uuid4()) + "_bw." + image.format.lower()
    # image_path = f"images/bw/{image_name}"
    # cv2.imwrite(image_path, wb_img)

    return Image.fromarray(wb_img)


def image_meta_data_extractor(image: Image):
    # extract other basic metadata
    info_dict = {
        "Filename": image.filename,
        "Image Size": image.size,
        "Image Height": image.height,
        "Image Width": image.width,
        "Image Format": image.format,
        "Image Mode": image.mode,
        "Image is Animated": getattr(image, "is_animated", False),
        "Frames in Image": getattr(image, "n_frames", 1),
    }

    return info_dict
