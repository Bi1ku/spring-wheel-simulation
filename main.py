from vpython import *

class Simulation: 
    def __init__(self, wheelR, axelR):
        self.wheel = Wheel(wheelR, 1.0, [vec(0, 0.25, 0), vec(0, -0.25, 0)])
        self.axis = Axis(axelR)

        self.axis.display()

    def loop(self):
        self.wheel.display()

class Wheel: 
    def __init__(self, radius, mass, springLocations):
        self.radius = radius 
        self.length = 1
        self.springLocations = springLocations
        self.calculateMomentOfInertia()

    def calculateMomentOfInertia(self):
        self.mInertia = (0.5 * self.mass * math.pow(self.radius, 2))

    def applyTorque(self, force, lArm):
        pass
    
    def changeMass(self, mass):
        self.mass = mass 
        calculateMomentOfInertia()

    def changeRadius(self, radius):
        self.radius = radius 
        calculateMomentOfInertia()
        
    def display(self):
        self.cylinder = cylinder(pos = vec(0, 0, 0), axis = vec(0, 0, 1), radius = self.radius, length = self.length, color = color.red)
        self.springPoints = points(pos = self.springLocations, color = color.gray)

        #self.cylinder.rotate(axis = vec(0,0,0), angle = pi/3)
class Axis:
    def __init__(self, radius):
        self.radius = radius 
        self.length = 1.5
    
    def display(self):
        cylinder(pos = vec(0, 0, 0), axis = vec(0, 0, 1), radius = self.radius, length = self.length, color = color.yellow)

if __name__ == "__main__":
    simulation = Simulation(0.5, 0.1)
    simulation.loop()
    