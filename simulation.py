from vpython import *
from spring import Spring
from wheel import Wheel
from axis import Axis
from pole import Pole
from constants import SCENE


class Simulation:
    def __init__(self, initSpringLength = 1.0, initSpringY = 0.8, initSpringConstant = 10, wheelMass = 1.0, wheelR = 0.5, axelR = 1.0):
        self.initSpring = Spring(initSpringLength, initSpringY, initSpringConstant) #temp
        self.springArr = [self.initSpring]
        self.wheel = Wheel(wheelR, wheelMass, self.springArr)
        self.axis = Axis(axelR)
        self.pole = Pole()

        self.axis.display()
        self.pole.display()
    
    def loop(self):
        self.wheel.display()
        for spring in self.springArr:
            spring.display()

    def setup(self):
        scene.background = color.white
        # make the scene not interactive (emulate 2D)

