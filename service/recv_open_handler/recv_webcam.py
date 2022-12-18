import io
import os
import time
from typing import BinaryIO

import cv2
import numpy
import userpaths
from PIL import Image

from service.recv_open_handler.recv_open_handler import RecvOpenHandler


class RecvWebcam(RecvOpenHandler):

    def process(self, msg: bytes) -> None:
        cv2.destroyAllWindows()
        imageStream = io.BytesIO(msg)
        img = Image.open(imageStream)
        cv2.imshow('image', cv2.cvtColor(numpy.array(img), cv2.COLOR_RGB2BGR))
        cv2.waitKey(1)

    def stop(self) -> None:
        pass
