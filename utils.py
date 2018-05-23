import cv2
import numpy as np
from skimage.morphology import skeletonize


def getContourOfImage(image, minVal=100, maxVal=200):
    """
    Get the contour of grayscale image of character by using the Canny Edge Detection algorithm.
    :param image: grayscale image of character.
    :param minVal: minimizing value of Hysteresis thresholding.
    :param maxVal: maximizing value of Hysteresis thresholding.
    :return: grayscale image of edge.
    """
    if image is None:
        return None
    # invert the color (background is black)
    image = 255 - image

    # use the Canny algorithm
    edge = cv2.Canny(image, minVal, maxVal)

    # invert the color of the edge image (black contour)
    edge = 255 - edge

    return edge


def getSkeletonOfImage(image):
    """
    Get skeleton of grayscale image.
    :param image:
    :return:
    """
    if image is None:
        return
    img_bit = image != 255
    skeleton = skeletonize(img_bit)
    skeleton = (1 - skeleton) * 255
    skeleton = np.array(skeleton, dtype=np.uint8)
    return skeleton


def createBlankGrayscaleImage(image):
    """
    Create blank grayscale image based on the reference image shape.
    :param image:
    :return:
    """
    if image is None:
        return
    img = np.ones_like(image) * 255
    img = np.array(img, dtype=np.uint8)

    return img