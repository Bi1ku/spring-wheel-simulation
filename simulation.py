from vpython import *
from spring import Spring
from wheel import Wheel
from axis import Axis
from pole import Pole
from constants import SCENE


class Simulation:
    def __init__(
        self,
        initSpringLength=300,
        initSpringY=0,
        initSpringConstant=10,
        wheelMass=1.0,
        wheelR=0.5,
        axelR=1.0,
    ):
        self.initSpring = Spring(
            initSpringLength, 50, initSpringY, initSpringConstant
        )  # temp
        self.springArr = [self.initSpring]

        self.wheel = Wheel(wheelR, wheelMass, self.springArr)
        self.axis = Axis(axelR)
        self.pole = Pole()

    def loop(self):
        self.wheel.update()
        for spring in self.springArr:
            spring.update()
        self.pole.update()

    def menu(self):
        def d_theta_bind(evt):
            print(evt.value)
            d_theta_text.text = "Ang Displ: " + str(evt.value) + " rad\n"

        SCENE.append_to_caption("Angular Displacement: ")
        d_theta = slider(bind=d_theta_bind, min=0, max=100, value=0, step=1, length=200)
        d_theta_text = wtext(text=str(d_theta.value) + " rad\n")

    def setup(self):
        SCENE.background = color.white

        self.wheel.display()
        self.pole.display()
        self.axis.display()
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
