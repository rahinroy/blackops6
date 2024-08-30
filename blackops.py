import time
import re
import cv2
import mss
import numpy as np
import easyocr 
from time import sleep

reader = easyocr.Reader(['en']) 
pattern = r'^[A-Z0-9]{4}-[A-Z0-9]{5}-[A-Z0-9]{4}$'


with mss.mss() as sct:
    # Part of the screen to capture 
    monitor = {"top": 400, "left": 570, "width": 190, "height": 50}
    codes_seen = set()
    while "Screen capturing":
        last_time = time.time()

        # Get raw pixels from the screen, save it to a Numpy array
        img = np.array(sct.grab(monitor))
        im_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        (thresh, im_bw) = cv2.threshold(im_gray, 180, 255, cv2.THRESH_BINARY)


        # Display the picture
        # cv2.imshow("OpenCV/Numpy normal", im_bw)

        result = reader.readtext(im_bw)
        result = [x[1] for x in result if x[2] > 0.8]
        for res in result:
            if (re.match(pattern, res) and res not in codes_seen):
                print(res)
                codes_seen.add(res)
        sleep(0.05)

        if cv2.waitKey(25) & 0xFF == ord("q"):
                # cv2.destroyAllWindows()
                break
