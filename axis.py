from vpython import *


class Axis:
    def __init__(self, radius):
        self.radius = radius
        self.length = 1.5

    def display(self):
        cylinder(
            pos=vec(0, 0, 0),
            axis=vec(0, 0, 1),
            radius=self.radius,
            length=self.length,
            color=color.yellow,
        )
