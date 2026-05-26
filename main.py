from vpython import *

NUM_SPRINGS = 1
scene = canvas(title="Wheel and Spring Simulation", width=800, height=600)
ROD_X = -scene.width + 50

class Simulation:

    def __init__(self, wheelMass = 1.0, wheelR = 0.5, axelR = 1.0):
        self.initSpring = Spring(1.0, 1.0, 10) #temp
        self.springArr = [self.initSpring]
        self.wheel = Wheel(wheelR, wheelMass, self.springArr)
        self.axis = Axis(axelR)
        self.pole = Pole()

        self.axis.display()

    def loop(self):
        self.wheel.display()
        self.spring.display()
        self.pole.display()

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
    def __init__(self, length, y_pos, spring_constant):
        self.spring_length = length
        self.equi_position = vector(ROD_X + 50, y_pos, 0)
        self.current_position = self.equi_position
        self.spring_constant = spring_constant
        
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

    def display(self):
        helix(
            pos=self.spring_position,
            axis=vec(1, 0, 0),
            color=color.cyan,
            radius=100,
            length=self.spring_length,
        )
    
    def getForce(self): 
        retun self.spring_constant * (self.current_position - self.equi_position)

class Wheel:
    def __init__(self, radius, mass, springs):
        self.radius = radius
        self.length = 1
        self.springs = springs
        self.mass = mass
        self.calculateMomentOfInertia()

    def calculateMomentOfInertia(self):
        pass 

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
        self.cylinder = cylinder(
            pos=vec(0, 0, 0),
            axis=vec(0, 0, 1),
            radius=self.radius,
            length=self.length,
            color=color.red,
        )
        self.springPoints = points(pos=self.springLocations, color=vec(0, 1, 0))

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
