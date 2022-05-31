import urllib
from learning_racer.config import ConfigReader

class RobotController():
    def __init__(self):
        self.MAX_MOTORLIMIT = 1.0
        self.MIN_MOTORLIMIT = 0.0
        self.config = ConfigReader()
        self.config.load()
        self.ip = self.config.rest_ip()
        self.port = self.config.rest_port()

    def action(self, steering, throttle):
        print('--------')
        steering = float(steering)
        throttle = float(throttle)
        left_motor_value = max(min(throttle + steering, self.MAX_MOTORLIMIT), self.MIN_MOTORLIMIT)
        right_motor_value = max(min(throttle - steering, self.MAX_MOTORLIMIT), self.MIN_MOTORLIMIT)
        print('Throttle: {0}'.format(throttle))
        print('Steering: {0}'.format(steering))
        req = urllib.request.urlopen('http://{0}:{1}/motors?left={2}&right={3}'.format(self.ip, self.port, left_motor_value, right_motor_value))
