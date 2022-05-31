import urllib
import numpy as np
import cv2
from PIL import Image
from learning_racer.config import ConfigReader

class Observer:

    def __init__(self, camera_width, camera_height):
        self.config = ConfigReader()
        self.config.load()
        self.ip = self.config.rest_ip()
        self.port = self.config.rest_port()

    def start(self):
        pass

    def stop(self):
        pass

    def _callback(self, change):
        pass

    def observation(self):
        req = urllib.request.urlopen('http://{0}:{1}/camera'.format(self.ip, self.port))
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        img = cv2.imdecode(arr, -1)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return img
