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

    m.click(int(x/MONITOR_X*MX),int(y/MONITOR_Y*MY))


def auto():

    start_p = cv2.imread('start.png', 0)
    start_yyh_p = cv2.imread('start_yyh.png', 0)

    end_p = cv2.imread('end.png', 0)
    finsih_p = cv2.imread('finish.png', 0)
    count = 0
    while True:
        r,x,y = find_pattern(start_p)
        if r:
            touch(x,y)
            print('识别了开始刷本的pattern，开始刷本 %d 次' % count)
            count += 1
            continue
        r, x, y = find_pattern(start_yyh_p)
        if r:
            touch(x,y)

            print('识别了开始刷业原火副本的pattern，开始刷本 %d 次' % count)
            count += 1
            continue
        r,x,y = find_pattern(end_p)
        if r:
            touch(x+200, y+50)
            print('识别了刷本结束的pattern')
            time.sleep(0.5)
            touch(x+200, y+50)
            continue

        r,x,y = find_pattern(finsih_p)
        if r:
            touch(x,y)
            print("x:%d,y:%d"%(x,y))
            print('一次刷本Finish')
            continue
# auto()

def react(pattern, response, t):
    r, x, y = find_pattern(pattern)
    if r:
        touch(x, y)
        print('%s'%response, t)

def auto_common():
    start_p = cv2.imread('start.png', 0)
    start_yyh_p = cv2.imread('start_yyh.png', 0)
    up_p = cv2.imread('up.png', 0)
    end_p = cv2.imread('end.png', 0)
    finsih_p = cv2.imread('finish.png', 0)
    while True:
        for i in range(3):
            r, x, y = find_pattern(up_p)
            if r:
                touch(x, y)
                print("x:%d,y:%d" % (x, y))
                print('一次刷本Finish')
                continue
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


def auto_rihefang():
    pipei_p = cv2.imread('tiaozhan.png', 0)
    zudui_p = cv2.imread('zudui.png', 0)
    zhunbei_p = cv2.imread('zhunbei.png', 0)
    start_p = cv2.imread('start.png', 0)
    finsih_p = cv2.imread('finish.png', 0)

    end2_p = cv2.imread('jixu2.png', 0)

    end_p = cv2.imread('jixu.png', 0)
    count = 0

    while True:

        img = get_picture()
        r, x, y = find_pattern(img, end_p)
        if r:
            touch(x, y)
            print('识别了刷本结束的pattern', 0.5)
            time.sleep(0.5)
            touch(x, y)
            continue
        r, x, y = find_pattern(img, end2_p)
        if r:
            touch(x, y)
            print('识别了刷本结束的pattern', 0.5)
            time.sleep(0.5)
            touch(x, y)
            continue
        r, x, y = find_pattern(img, zudui_p)
        if r:
            touch(x, y)
            print('组队完成')

            continue
        r, x, y = find_pattern(img, pipei_p)
        if r:
            touch(x, y)
            print('开始匹配')
            continue
        r, x, y = find_pattern(img, start_p)
        if r:
            touch(x, y)
            print('开始挑战')
            continue
        r, x, y = find_pattern(img, zhunbei_p, 0.5)
        if r:
            touch(x, y)

            print('准备完成，开始刷本 %d 次' % count)
            count += 1
            continue
        r,x,y = find_pattern(img, finsih_p)
        if r:
            touch(x,y)
            print("x:%d,y:%d"%(x,y))
            print('一次刷本Finish')
            continue
def auto_rihefang_mt():
    pipei_p = cv2.imread('tiaozhan.png', 0)
    zudui_p = cv2.imread('zudui.png', 0)
    zhunbei_p = cv2.imread('zhunbei.png', 0)
    start_p = cv2.imread('start.png', 0)
    finsih_p = cv2.imread('finish.png', 0)

    end2_p = cv2.imread('jixu2.png', 0)

    end_p = cv2.imread('jixu.png', 0)


    while True:
        img = get_picture()
        threads = []
        result_list = []
        threads.append(pattern_thread(img, end_p,0.5))
        threads.append(pattern_thread(img, end2_p,0.5))
        threads.append(pattern_thread(img, zudui_p))
        threads.append(pattern_thread(img, pipei_p))
        threads.append(pattern_thread(img, start_p))
        threads.append(pattern_thread(img, zhunbei_p,0.5))
        threads.append(pattern_thread(img, finsih_p))
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        for t in threads:
            if t.result[0]:
                touch(t.result[1],t.result[2])
                break
        time.sleep(0.5)
auto_rihefang_mt()
# auto_common()