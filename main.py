from vpython import *

NUM_SPRINGS = 1
scene = canvas(title="wheel and spring", width=800, height=600)
ROD_X = -scene.width + 50

class Simulation:
    def __init__(self, initSpringLength = 1.0, initSpringY = 0.8, initSpringConstant = 10, wheelMass = 1.0, wheelR = 0.5, axelR = 1.0):
        self.initSpring = Spring(initSpringLength, initSpringY, initSpringConstant) #temp
        self.springArr = [self.initSpring]
        self.wheel = Wheel(wheelR, wheelMass, self.springArr)
        self.axis = Axis(axelR)
        self.pole = Pole()

        self.axis.display()
        self.pole.display()
    
    def loop(self):
        self.wheel.display()
        for spring in self.springArr:
            spring.display()

    def setup(self):
        scene.background = color.white
        # make the scene not interactive (emulate 2D)


class Pole:
    def __init__(self):
        pass

    def display(self):
        curve(
            pos=[
                vec(ROD_X, scene.height, 0),
                vec(ROD_X, -scene.height, 0),
            ],
            color=color.black,
            radius=10,
        )

class Spring:
    def __init__(self, length, yPos, springConstant):
        self.springLength = length
        self.leverArm = vector(0, yPos, 0)
        self.equiPosition = vector(ROD_X + 50, yPos, 0)
        self.currentPosition = self.equiPosition
        self.springConstant = springConstant
        
    @staticmethod
    def bind_num_springs(evt):
        print(evt.value)
        NUM_SPRINGS = evt.value

    @staticmethod
    def bind_len_springs(evt):
        if evt.id == "1":
            pass
        elif evt.id == "2":
            pass
        elif evit.id == "3":
            pass

    def changePosition(self, position): #not for slider use, must be vector
        self.currentPosition = position

    def changeConstant(self, constant):
        self.springConstant = constant

    def display(self):
        helix(
            pos=self.currentPosition,
            axis=vec(1, 0, 0),
            color=color.cyan,
            radius=100,
            length=self.springLength,
        )
    
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
        #self.springPoints = points(pos=self.springLocations, color=vec(0, 1, 0))

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


if __name__ == "__main__":
    simulation = Simulation()
    simulation.setup()
    simulation.loop()
