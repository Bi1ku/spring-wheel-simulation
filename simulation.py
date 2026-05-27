from vpython import *
from spring import Spring
from wheel import Wheel
from pole import Pole
from constants import SCENE
import math


class Simulation:
    def __init__(
        self,
        initSpringLength=300,
        initSpringY=0,
        initSpringConstant=10,
        wheelMass=1.0,
        wheelR=100,
    ):
        self.initSpring = Spring(
            initSpringLength, 50, initSpringY, initSpringConstant
        )  # temp
        self.springArr = [self.initSpring]

        self.wheel = Wheel(wheelR, wheelMass, self.springArr)
        self.pole = Pole()
        self.d_theta = 0

    def loop(self):
        self.wheel.update()
        for spring in self.springArr:
            spring.update(self.d_theta, self.wheel.radius)
        self.pole.update()

    def menu(self):
        def d_theta_bind(evt):
            d_theta_text.text = "Ang Displ: " + str(evt.value) + " rad\n"
            self.d_theta = evt.value

        SCENE.append_to_caption("Angular Displacement: ")
        slider(
            bind=d_theta_bind,
            min=0,
            max=math.radians(30),
            value=self.d_theta,
            step=math.radians(0.1),
            length=200,
        )
        d_theta_text = wtext(text=str(self.d_theta) + " rad\n")

    def setup(self):
        SCENE.background = color.white

        self.wheel.display()
        self.pole.display()
        for spring in self.springArr:
            spring.display()
        self.menu()

        SCENE.center = vec(0, 0, 0)
        SCENE.forward = vec(0.407, -0.00999, -0.913)
        SCENE.up = vec(0, 1, 0)
        SCENE.range = 660

        SCENE.userzoom = False
        SCENE.userspin = False
        SCENE.userpan = False

        rate(60)
