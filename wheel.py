from vpython import *
from constants import WHEEL_CENTER_X, WHEEL_CENTER_Y



class Wheel:
    def __init__(self, radius, mass, springs, extrusion=None, points=[]):
        self.points = points
        self.extrusion = extrusion
        self.springs = springs
        self.mass = mass
        self.time = 0.0

        self.wheel = cylinder(pos=vec(WHEEL_CENTER_X, WHEEL_CENTER_Y, 0),axis=vec(WHEEL_CENTER_X, WHEEL_CENTER_Y, -1),radius=radius,length=1,color=color.red,make_trail=True)

        spoke1 = curve(pos=[vec(0, 0, 0), vec(radius, 0, 0)],color=color.black,radius=5)

        spoke2 = curve(pos=[vec(0, 0, 0), vec(0, radius, 0)],color=color.black,radius=5)

        spoke3 = curve(pos=[vec(0, 0, 0), vec(-radius, 0, 0)],color=color.black,radius=5)

        spoke4 = curve(pos=[vec(0, 0, 0), vec(0, -radius, 0)],color=color.black,radius=5)

        self.spokes = [spoke1, spoke2, spoke3, spoke4]

        # self.springPoints = points(pos=self.springs, color=vec(0, 1, 0))

        self.calculateMomentOfInertia()

    def calculate_area(self):
        # using shoelace formula
        left_sum = 0
        right_sum = 0

        if self.extrusion is not None:
            for i in range(len(self.points)):
                j = 0 if i == len(self.points) - 1 else i + 1
                left_sum += self.points[i][0] * self.points[j][1]
                right_sum += self.points[j][0] * self.points[i][1]

        return (0.5 * abs(left_sum - right_sum), 0.5 * (left_sum - right_sum))
    
    def calculate_com(self):
        # for two dimensional shapes, centroid is the center of mass
        # use a new formula for centroid of 2D polygon w/ shoelace 
        # can use this later in parallel axis theorem

        x_sum = 0
        y_sum = 0
        for i in range(len(self.points)):
            j = 0 if i == len(self.points) - 1 else i + 1
            x_sum += (self.points[i][0] + self.points[j][0]) * (self.points[i][0] * self.points[j][1] - self.points[j][0] * self.points[i][1])
            y_sum += (self.points[i][1] + self.points[j][1]) * (self.points[i][0] * self.points[j][1] - self.points[j][0] * self.points[i][1])
        
        area = self.calculate_area()[1] # signed area
        sphere(pos=vec(x_sum / (6 * area), y_sum / (6 * area), 0), radius=10, color=color.green)
        return vec(x_sum / (6 * area), y_sum / (6 * area), 0)

    def calculateMomentOfInertia(self):
        if self.extrusion is not None:
            # Calculate area moment of inertia for the shape about the x-axis
            # Calculate area moment of inertia for the shape about the y-axis
            # Using those, find the area moment of inertia about of the z-axis
            # Use parallel-axis theorem and com (centroid) to find the moment of inertia about the center of mass or some other point
            density = self.mass / self.calculate_area()[0]
            pass
        else:
            self.momentOfInertia = 0.5 * self.mass * pow(self.wheel.radius, 2)

    def change_config(self, evt, theta=0):
        if evt.id == "mass":
            print(self.calculate_area())
            print(self.calculate_com())
            self.mass = evt.value

        elif evt.id == "radius" and not self.extrusion:
            self.wheel.radius = evt.value
            self.spokes[0].modify(1, pos=vec(evt.value, 0, 0))
            self.spokes[1].modify(1, pos=vec(0, evt.value, 0))
            self.spokes[2].modify(1, pos=vec(-evt.value, 0, 0))
            self.spokes[3].modify(1, pos=vec(0, -evt.value, 0))

        elif evt.id == "d_theta":
            self.update_position(theta)

        self.calculateMomentOfInertia()

    def update_position(self, theta):
        for spoke in self.spokes:
            spoke.rotate(angle=-theta,axis=vec(0, 0, 1),origin=vec(0, 0, 0))

    def calculate_angular_frequency(self):
        """
        let me cook here
        t = torque
        a = angular acceleration
        l = lever arm for spring

        t = I * a
        -k(l * theta) x l = 0.5 * m * r^2 * a
        (-k*l^2)/(0.5 * m*r^2) * theta = a
        so we only need to get the sum of all -k * l^2 (still need to consider them as vectors) to calculate angular frequency
        """

        total_components = 0
        for spring in self.springs:
            total_components += spring.get_angular_frequency_component().z

        w_squared = abs(total_components / self.momentOfInertia)
        return sqrt(w_squared)

    def calculate_angular_accel(self):

        total_torque = 0

        for spring in self.springs:
            # print(spring.left_y_level);
            total_torque += spring.get_torque().z

        return total_torque / self.momentOfInertia

    # def update(self):
    # where the actual simulation goes
    # self.springPoints = points(pos=self.springLocations, color=vec(0, 1, 0))
    # pass
