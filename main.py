from vpython import *

class Simulation: 
    def __init__(self, wheelR, axelR):
        self.wheel = Wheel(wheelR)
        self.axis = Axis(axelR)
        self.axis.display()

    def loop(self):
        self.wheel.display()

class Wheel: 
    def __init__(self, radius):
        self.radius = radius 
        self.length = 1
    
    def display(self):
        cylinder(pos = vec(0, 0, 0), axis = vec(0, 0, 1), radius = self.radius, length = self.length, color = color.red)

class Axis:
    def __init__(self, radius):
        self.radius = radius 
        self.length = 1.5
    
    def display(self):
        cylinder(pos = vec(0, 0, 0), axis = vec(0, 0, 1), radius = self.radius, length = self.length, color = color.yellow)

if __name__ == "__main__":
    simulation = Simulation(0.5, 0.1)
    simulation.loop()
    