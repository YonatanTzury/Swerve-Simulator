import logging
import math
import numpy as np
import pygame # type: ignore

import utils
from wheel import Wheel
from joystick import Joystick

# Units:
#     Distance - Pixel
#     Time - Frame (1/30 Sec)
#     Angle - Radians
#     Angular velocity - radians / frame
#     Linear velocity - Pixel / frame

# Directions/angles always stored as unit vector angle
# The wheel module use a speed + direction instead of velocity vector to represent "real" wheel
#      Also a real wheel velocity can be just vector

class Swerve(object):
    def __init__(self, width: int, hight: int) -> None:
        self._v = np.array([1, 1]) 
        self._w = 0.2

        self._width = width

        right = width / 2
        left = -right
        bottom = hight / 2
        top = -bottom

        self._wheels = [
            (Wheel('Top Left', 0, 0), np.array([left, top])),
            (Wheel('Top Right', width, 0), np.array([right, top])),
            (Wheel('Bottom Left', 0, hight), np.array([left, bottom])),
            (Wheel('Bottom Right', width, hight), np.array([right, bottom]))
        ]
        print(self._wheels)

    def get_center(self):
        # Middle of diagonal (top left <> bottom right)
        return (self._wheels[0][0]._pos + self._wheels[-1][0]._pos) / 2

    def get_heading(self):
        # Direction of "Top Right" <> "Top Left", normalize by the width
        # The heading is perallal to the top bottom lines
        return (self._wheels[1][0]._pos - self._wheels[0][0]._pos) / self._width

    def calc_pod_params(self, diff):
        # v = v_0 + W X R
        # self._v is a vector repesent the velocity of the robot (speend and direction)
        # self.w is a vector represent the angular velocity of the robot (speed and direction)
        # diff represent the radion of movement (between robot center to the cur wheel)

        v = np.append(self._v, 0)
        w = np.array([0, 0, self._w])
        r = np.append(diff, 0)

        velocity = v + np.cross(w, r)
        speed = np.linalg.norm(velocity)
        direction = velocity / speed

        return speed, direction[:2]

    def do_step(self) -> None:
        for wheel, diff in self._wheels:
            # angle = math.atan(diff[1]/diff[0]) + math.atan(self.get_heading()[1]/self.get_heading()[0])
            # real_diff = np.array([math.cos(angle), math.sin(angle)])
            real_diff = wheel._pos - self.get_center()
            speed, direction = self.calc_pod_params(real_diff)

            wheel.set_speed(speed)
            wheel.set_direction(direction)
            wheel.do_step()

    def draw(self, screen) -> None:
        logging.debug(f'SWERVE - c: {self.get_center()}, h: {self.get_heading()}')

        utils.draw_circle(screen, self.get_center(), 10, 'green', self.get_heading(), 'white')

        colors = ['yellow', 'purple', 'brown', 'white']
        i = 0
        for wheel, diff in self._wheels:
            print(diff)
            pygame.draw.line(screen, colors[i], self.get_center(), self.get_center() + diff)
            wheel.draw(screen)
            i += 1


def main():
    logging.basicConfig(level=logging.DEBUG)

    swerve = Swerve(80, 80)
    joystick = Joystick(120, 520)
    
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True

    while running:
        swerve.do_step()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('Exiting')
                running = False

        screen.fill('black')
        joystick.draw(screen)
        swerve.draw(screen)

        pygame.display.flip()
        clock.tick(10)

    while True:
        import time; time.sleep(1)
    pygame.quit()

if __name__ == '__main__':
    main()