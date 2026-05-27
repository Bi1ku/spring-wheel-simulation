from vpython import *
from spring import Spring
from wheel import Wheel
from axis import Axis
from pole import Pole
from constants import SCENE


class Simulation:
    def __init__(self, wheelR, axelR):
        self.spring = Spring(300, 50, 10, 10)
        self.wheel = Wheel(wheelR, 1.0, [vec(0, 0.25, 0), vec(0, -0.25, 0)])
        self.axis = Axis(axelR)
        self.pole = Pole()

    def loop(self):
        self.wheel.update()
        self.spring.update()
        self.pole.update()

    def setup(self):
        SCENE.background = color.white

        self.wheel.display()
        self.spring.display()
        self.pole.display()
        self.axis.display()

        SCENE.center = vec(0, 0, 0)
        SCENE.forward = vec(0.407, -0.00999, -0.913)
        SCENE.up = vec(0, 1, 0)
        SCENE.range = 660

        SCENE.userzoom = False
        SCENE.userspin = False
        SCENE.userpan = False

        rate(60)
