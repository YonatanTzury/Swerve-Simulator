import pygame
import numpy as  np

import utils


class Joystick(object):

    def __init__(self, x: float, y: float) -> None:
        self._center = np.array([float(x), float(y)])

    def get_angle(self) -> float:
        mouse_pos = pygame.mouse.get_pos()
        direction_vector = mouse_pos - self._center
        return direction_vector / np.linalg.norm(direction_vector)

    def draw(self, screen) -> None:
        utils.draw_circle(screen, self._center, 30, 'blue', self.get_angle(), 'white')
