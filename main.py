from vpython import *

class Simulation: 
    def __init__(self, wheelR, axelR):
        self.wheel = Wheel(wheelR, 1.0, [vec(0, 0.25, 0), vec(0, -0.25, 0)])
        self.axis = Axis(axelR)

        self.axis.display()

    def loop(self):
        self.wheel.display()

class Wheel: 
    def __init__(self, radius, mass, springs):
        self.radius = radius 
        self.length = 1
        self.springs = springs
        self.mass = mass
        self.calculateMomentOfInertia()

    def calculateMomentOfInertia(self):
        self.mInertia = (0.5 * self.mass * pow(self.radius, 2))

    def applyTorques(self):
        netTorqueMag = 0

        for spring in self.springs:
            force = spring.getForce() # method should return vector
            

    def changeMass(self, mass):
        self.mass = mass 
        calculateMomentOfInertia()

    def changeRadius(self, radius):
        self.radius = radius 
        calculateMomentOfInertia()
        
    def display(self):
        self.cylinder = cylinder(pos = vec(0, 0, 0), axis = vec(0, 0, 1), radius = self.radius, length = self.length, color = color.red)
        self.springPoints = points(pos = self.springs, color = color.green)
        print("hi")
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
    