from vpython import *
from spring import Spring
from wheel import Wheel
from pole import Pole
from constants import SCENE
import math


class Simulation:
    def __init__(self):
        self.run = False
        self.reset = False

        self.d_theta = 0
        self.mass = 15
        self.radius = 100
        self.spr_const = 1
        self.spr_wheel_dist = 0

        self.initSpring = Spring(300, 30, self.spr_wheel_dist, self.spr_const)
        self.spring_arr = [self.initSpring]

        self.wheel = Wheel(self.radius, self.mass, self.spring_arr)
        self.pole = Pole()

    def loop(self):
        self.wheel.update()
        for spring in self.spring_arr:
            spring.update(self.d_theta, self.wheel.radius)
        self.pole.update()

    def setup(self):
        SCENE.background = color.white

        self.wheel.display()
        self.pole.display()
        for spring in self.spring_arr:
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

    def menu(self):
        SCENE.append_to_caption("\n\n")

        ### RESET SIM BUTTON ###
        def bind_run(_):
            self.run = True

        button(bind=bind_run, text="Run Simulation")

        SCENE.append_to_caption("   ")

        ### RUN SIM BUTTON ###
        def bind_reset(_):
            self.reset = True

        button(bind=bind_reset, text="Reset Simulation")

        SCENE.append_to_caption("\n\n")

        ### ANGULAR DISPLACEMENT SLIDER ###
        def d_theta_bind(evt):
            d_theta_text.text = str(evt.value) + " rad\n"
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

        ### MASS SLIDER ###
        def mass_bind(evt):
            mass_text.text = str(evt.value) + " kg\n"
            self.mass = evt.value

        SCENE.append_to_caption("Wheel Mass: ")
        slider(
            bind=mass_bind,
            min=5,
            max=30,
            value=self.mass,
            step=0.5,
            length=200,
        )
        mass_text = wtext(text=str(self.mass) + " kg\n")

        ### WHEEL RADIUS SLIDER ###
        def radius_bind(evt):
            radius_text.text = str(evt.value) + " m\n"
            self.radius = evt.value

        SCENE.append_to_caption("Wheel Radius: ")
        slider(
            bind=radius_bind,
            min=50,
            max=150,
            value=self.radius,
            step=1,
            length=200,
        )
        radius_text = wtext(text=str(self.radius) + " m\n")

        ### SPRING CONSTANT SLIDER ###
        def spr_const_bind(evt):
            spr_const_text.text = str(evt.value) + " N/m\n"
            self.spr_const = evt.value

        SCENE.append_to_caption("Spring Constant: ")
        slider(
            bind=spr_const_bind,
            min=0.5,
            max=5,
            value=self.spr_const,
            step=0.1,
            length=200,
        )
        spr_const_text = wtext(text=str(self.spr_const) + " N/m\n")

        ### SPRING-WHEEL DISTANCE SLIDER ###
        def spr_wheel_dist_bind(evt):
            spr_wheel_dist_text.text = str(evt.value) + " m\n"
            self.spr_wheel_dist = evt.value

        SCENE.append_to_caption("Spring-Wheel Distance: ")
        slider(
            bind=spr_wheel_dist_bind,
            min=0,
            max=self.radius,
            value=self.spr_wheel_dist,
            step=1,
            length=200,
        )
        spr_wheel_dist_text = wtext(text=str(self.spr_wheel_dist) + " m\n")
