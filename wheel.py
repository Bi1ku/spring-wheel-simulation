from vpython import *


class Wheel:
    def __init__(self, radius, mass, springLocations):
        self.radius = radius
        self.length = 1
        self.springLocations = springLocations
        self.calculateMomentOfInertia()

    def calculateMomentOfInertia(self):
        # self.mInertia = 0.5 * self.mass * math.pow(self.radius, 2)
        pass

    def applyTorque(self, force, lArm):
        pass

    def changeMass(self, mass):
        self.mass = mass
        calculateMomentOfInertia()

    def changeRadius(self, radius):
        self.radius = radius
        calculateMomentOfInertia()

    def display(self):
        self.cylinder = cylinder(
            pos=vec(0, 0, 0),
            axis=vec(0, 0, 1),
            radius=self.radius,
            length=self.length,
            color=color.red,
        )
        self.springPoints = points(pos=self.springLocations, color=vec(0, 1, 0))
