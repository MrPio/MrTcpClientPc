import pickle
import struct
import sys
import time
from ctypes import sizeof

import cv2
from PIL import Image

vid = cv2.VideoCapture(0)
while(vid.isOpened()):
    start=time.time_ns()
    _,frame = vid.read()
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    im_pil = Image.fromarray(img)
    im_pil.save('img.jpg', optimize=True, quality=20)

    # a = pickle.dumps(frame)
    # print(f'pickle - {sys.getsizeof(a)}')

    # message = struct.pack("L",len(a))+a
    # print(f'struct - {sys.getsizeof(message)}')

    # client_socket.sendall(message)
    # cv2.imshow('Sending...',frame)
    key = cv2.waitKey(10)
    print(time.time_ns()-start)

