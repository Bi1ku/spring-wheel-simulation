from vpython import *

ROD_X = -screen.width + 10
NUM_SPRINGS = 1


def bind_num_springs(evt):
    print(evt.value)
    NUM_SPRINGS = evt.value


def bind_len_springs(evt):
    if evt.id == "1":
        pass
    elif evt.id == "2":
        pass
    elif evit.id == "3":
        pass


class Spring:
    def __init__(self, length, y_pos, spring_constant):
        self.spring_length = length
        self.spring_position = vector(ROD_X, y_pos, 0)
        self.spring_constant = spring_constant

    def draw(self):
        helix(
            pos=self.spring_position,
            axis=vec(1, 0, 0),
            color=color.cyan,
            radius=100,
            length=self.spring_length,
        )


def menu():
    slider(bind=bind_num_springs, max=3, min=1, step=1, value=NUM_SPRINGS)


def setup():
    scene.background = color.white
    menu()
    curve(
        pos=[vec(ROD_X, -screen.height, 0), vector(ROD_X, screen.height, 0)],
        color=color.black,
        radius=10,
    )
    spring = Spring(100, 6, 10)
    spring.draw()


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
        #print("hi")
        #self.cylinder.rotate(axis = vec(0,0,0), angle = pi/3)

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
    simulation = Simulation(0.5, 0.1)
    simulation.loop()
