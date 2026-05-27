from vpython import *


class Wheel:
    def __init__(self, radius, mass, springs):
        self.radius = radius
        self.length = 1
        self.springs = springs
        self.mass = mass
        self.calculateMomentOfInertia()

    def calculateMomentOfInertia(self):
        self.momentOfInertia = 0.5 * self.mass * pow(self.radius, 2)

    def changeMass(self, mass):
        self.mass = mass
        calculateMomentOfInertia()

    def changeRadius(self, radius):
        self.radius = radius
        calculateMomentOfInertia()

    def display(self):
        cylinder(
            pos=vec(0, 0, 0),
            axis=vec(0, 0, 1),
            radius=self.radius,
            length=self.length,
            color=color.red,
        )
        # self.springPoints = points(pos=self.springLocations, color=vec(0, 1, 0))

    def update(self):
        pass
        # self.springPoints = points(pos=self.springLocations, color=vec(0, 1, 0))
