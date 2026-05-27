from vpython import *
from spring import Spring
from wheel import Wheel
from axis import Axis
from pole import Pole
from constants import SCENE


class Simulation:
    def __init__(self, wheelR, axelR):
        self.spring = Spring(100, 6, 10)
        self.wheel = Wheel(wheelR, 1.0, [vec(0, 0.25, 0), vec(0, -0.25, 0)])
        self.axis = Axis(axelR)
        self.pole = Pole()

        self.axis.display()

    def loop(self):
        self.wheel.display()
        self.spring.display()
        self.pole.display()

    def setup(self):
        SCENE.background = color.white
        # make the scene not interactive (emulate 2D)
