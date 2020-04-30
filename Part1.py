import cv2 
from matplotlib import pyplot as plt
import numpy as np

def plt_show0(*b):
    '''显示一个彩色的图片，这个图片必须是一个array'''
    for img in b:
        plt.imshow(img)
        plt.show()

def plt_show(*b):
    '''显示一个只有灰度的图片'''
    for img in b:
        plt.imshow(img,cmap='gray')
        plt.show()

def img_read(path):
    '''读取图片'''
    image = cv2.imread(path)
    b,g,r = cv2.split(image)
    image = cv2.merge([r,g,b])
    
    return image

def gray_guss(image):
    '''高斯灰度处理'''
    image = cv2.GaussianBlur(image, (3, 3), 0)
    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    
    return gray_image

def get_carLicense_img(image):
    '''获取车牌'''
    origin_image = image.copy()
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (17, 5))
    kernelX = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 1))
    kernelY = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 19))
    
    gray_image = gray_guss(image)
    Sobel_x = cv2.Sobel(gray_image, cv2.CV_16S, 1, 0)
    image = cv2.convertScaleAbs(Sobel_x)
    ret, image = cv2.threshold(image, 0, 255, cv2.THRESH_OTSU)
    
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernelX,iterations = 3)
    image = cv2.dilate(image, kernelX)
    image = cv2.erode(image, kernelX)
    image = cv2.erode(image, kernelY)
    image = cv2.dilate(image, kernelY)
    image = cv2.medianBlur(image, 15)
    
    none,contours, hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for item in contours:
        rect = cv2.boundingRect(item)
        x = rect[0]
        y = rect[1]
        w = rect[2]
        h = rect[3]
        B = w/h
        if  3<B<4 :
            image = origin_image[y:y + h, x:x + w]
            return image
