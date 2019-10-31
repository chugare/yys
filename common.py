from settings import *
from PIL import ImageGrab
import cv2
from pymouse import PyMouse
import numpy as np
import time
import threading
bbox = (0, 0, 2560, 1440)
THRESHOLD = 0.9
m = PyMouse()
MX,MY = m.screen_size()
def get_picture():
    im = ImageGrab.grab(bbox)
    im.save('np.png')
    img = cv2.imread('np.png', 0)
    return img

def find_pattern(img , pattern,threshold = THRESHOLD):

    res = cv2.matchTemplate(img, pattern, cv2.TM_CCOEFF_NORMED)
    maxres = res.max()
    if maxres < threshold:
        return False, -1, -1
    pos = np.where(res == maxres)
    dx = pattern.shape[1] /2
    dy = pattern.shape[0] /2
    return True, int(pos[1][0] + dx), int(pos[0][0] + dy)


def match(img1, template):
    """img1代表待匹配图像, img2代表模板"""
    res = cv2.matchTemplate(img1, template, cv2.TM_CCOEFF_NORMED)
    maxres = res.max()
    return maxres


def touch(x,y):
    print((x,y))

    m.press(int(x/MONITOR_X*MX),int(y/MONITOR_Y*MY))

class pattern_thread(threading.Thread):
    def __init__(self, img, pattern, threashold=THRESHOLD, fun=None ):
        threading.Thread.__init__(self)
        self.img = img
        self.threashold = threashold
        self.pattern = pattern
        self.fun = fun
    def run(self):
        if self.fun:
            self.fun(self.pattern,self.threashold)
            return
        r,x,y = find_pattern(self.img, self.pattern, self.threashold)
        self.result = (r,x,y)
