import cv2
import time
from common import get_picture,pattern_thread,touch

def auto_dayuewan_mt():
    ready_p = cv2.imread('ready.png', 0)
    start_p = cv2.imread('start.png', 0)
    finsih_p = cv2.imread('finish.png', 0)
    end_p = cv2.imread('end.png', 0)
    dajiuma_p = cv2.imread('dajiuma.png', 0)
    focus_p = cv2.imread('focus.png', 0)
    while True:
        img = get_picture()
        threads = []
        result_list = []
        threads.append(pattern_thread(img, end_p,0.7))
        threads.append(pattern_thread(img, focus_p,0.7))
        threads.append(pattern_thread(img, dajiuma_p,0.7))
        threads.append(pattern_thread(img, ready_p,0.7))
        threads.append(pattern_thread(img, start_p))
        threads.append(pattern_thread(img, finsih_p))
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        focused = False
        for i,t in enumerate(threads):
            if t.result[0]:
                if i == 1:
                    break
                if i == 2 and not focused:
                    touch(t.result[1], t.result[2]+50)
                    break
                touch(t.result[1],t.result[2])
                break
        time.sleep(1)

if __name__ == '__main__':
    auto_dayuewan_mt()