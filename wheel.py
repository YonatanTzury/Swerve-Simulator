import math
import logging
import numpy as np

import utils

class Wheel(object):
    MAX_SPEED = 100
    MAX_ANGLE = math.pi * 2

    def __init__(self, name: str, x :float, y: float) -> None:
        self._speed = 0
        self._direction = 0
        self._name = name

        self._pos = np.array([float(x), float(y)])

    def set_speed(self, speed: float) -> None:
        if speed < 0:
            raise Exception('Negative speed is not allowd')

        if speed > self.MAX_SPEED:
            raise Exception(f'Speed larger then MAX_SPEED is not allowd: {speed}')

        self._speed = speed
        
    def set_direction(self, direction) -> None:
        # TODO keep the angle between 0 to 2pi
        self._direction = direction

    def do_step(self):
        self._pos += self._direction * self._speed

    def draw(self, screen) -> None:
        logging.debug(f'WHEEL: {self._name} - pos: {self._pos}, v: {self._speed}, a: {self._direction}')

        utils.draw_circle(screen, self._pos, 10, 'red', self._direction, 'blue')
