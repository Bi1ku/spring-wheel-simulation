from vpython import *

AXIS = (0, 0, 0)

class Wheel: 
    def __init__(self, radius):
        cylinder(pos = vec(0, 0, 0), axis = vec(0, 0, 1), radius = radius, color = color.red)

if __name__ == "__main__":
    wheel = Wheel(2)
