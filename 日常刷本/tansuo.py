from common import get_picture,touch,find_pattern,pattern_thread
import cv2
from pymouse import PyMouse
import numpy as np
import time
import threading

def auto_tansuo():
    jieshou_p = cv2.imread('gou.png', 0)
    end_p = cv2.imread('end.png', 0)
    back_p = cv2.imread('back.png', 0)
    confirm_p = cv2.imread('confirm.png', 0)
    flag_p = cv2.imread('flag.png', 0)
    count = 0
    class syn:
        def __init__(self):
            self.state = 0
        def set_state(self,value):
            self.state = value
    st = syn()
    def set_flag():
        st.set_state(1)

    def reset_flag():
        st.set_state(0)
    while True:

        img = get_picture()
        threads = []
        result_list = []

        threads.append(pattern_thread(img, end_p))
        threads.append(pattern_thread(img, jieshou_p))
        threads.append(pattern_thread(img, flag_p, 0.5))
        threads.append(pattern_thread(img, back_p))
        threads.append(pattern_thread(img, confirm_p))
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        for i,t in enumerate(threads):
            if t.result[0]:
                if i == 0:
                    touch(t.result[1]+200, t.result[2]+50)
                    break
                elif i == 2:
                    set_flag()

                elif i == 3:
                    if st.state == 1:
                        touch(t.result[1], t.result[2])
                        reset_flag()
                else:
                    touch(t.result[1], t.result[2])
                    break
        time.sleep(0.5)
auto_tansuo()