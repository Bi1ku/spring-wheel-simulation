from vpython import *

NUM_SPRINGS = 1


class Simulation:
    def __init__(self, wheelR, axelR):
        self.spring = Spring(100, 6, 10)
        self.wheel = Wheel(wheelR, 1.0, [vec(0, 0.25, 0), vec(0, -0.25, 0)])
        self.axis = Axis(axelR)
        self.pole = Pole()

        self.axis.display()

    def loop(self):
        self.wheel.display()
        self.spring.display()
        self.pole.display()

    def setup(self):
        scene.background = color.white


class Pole:
    def __init__(self):
        pass

    def display(self):
        curve(
            pos=[
                vec(-390, -390, 0),
                vec(-390, 390, 0),
            ],
            color=color.black,
            radius=10,
        )


class Spring:
    def __init__(self, length, y_pos, spring_constant):
        self.spring_length = length
        self.spring_position = vector(-390, y_pos, 0)
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
    simulation.setup()
    simulation.loop()
