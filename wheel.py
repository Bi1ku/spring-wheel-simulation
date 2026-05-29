from vpython import *
from constants import WHEEL_CENTER_X, WHEEL_CENTER_Y


class Wheel:
    def __init__(self, radius, mass, springs):
        self.springs = springs
        self.mass = mass
        self.time = 0.0

        self.wheel = cylinder(
            pos=vec(WHEEL_CENTER_X, WHEEL_CENTER_Y, 0),
            axis=vec(WHEEL_CENTER_X, WHEEL_CENTER_Y, -1),
            radius=radius,
            length=1,
            color=color.red,
            opacity=0.5,
            make_trail=True,
        )

        spoke1 = curve(
            pos=[vec(0, 0, 0), vec(radius, 0, 0)],
            color=color.black,
            radius=5,
        )

        spoke2 = curve(
            pos=[vec(0, 0, 0), vec(0, radius, 0)],
            color=color.black,
            radius=5,
        )

        spoke3 = curve(
            pos=[vec(0, 0, 0), vec(-radius, 0, 0)],
            color=color.black,
            radius=5,
        )

        spoke4 = curve(
            pos=[vec(0, 0, 0), vec(0, -radius, 0)],
            color=color.black,
            radius=5,
        )

        self.spokes = [spoke1, spoke2, spoke3, spoke4]

        # self.springPoints = points(pos=self.springs, color=vec(0, 1, 0))

        self.ang_pos_graph = graph(
            title="Angular Position vs Time",
            xtitle="Time (s)",
            ytitle="Angular Position (rad)",
            xmin=0.1,
        )
        self.ang_pos_curve = gcurve(color=color.blue)
        self.ang_vel_graph = graph(
            title="Angular Velocity vs Time",
            xtitle="Time (s)",
            ytitle="Angular Velocity (rad/s)",
            xmin=0.1,
        )
        self.ang_vel_curve = gcurve(color=color.green)
        self.ang_acc_graph = graph(
            title="Angular Acceleration vs Time",
            xtitle="Time (s)",
            ytitle="Angular Acceleration (rad/s^2)",
            xmin=0.1,
        )
        self.ang_acc_curve = gcurve(color=color.orange)
        self.prev_ang_freq = 0

        self.calculateMomentOfInertia()

    def calculateMomentOfInertia(self):
        self.momentOfInertia = 0.5 * self.mass * pow(self.wheel.radius, 2)

    def change_config(self, evt, theta=0):
        if evt.id == "mass":
            self.mass = evt.value

        elif evt.id == "radius":
            self.wheel.radius = evt.value
            self.spokes[0].modify(1, pos=vec(evt.value, 0, 0))
            self.spokes[1].modify(1, pos=vec(0, evt.value, 0))
            self.spokes[2].modify(1, pos=vec(-evt.value, 0, 0))
            self.spokes[3].modify(1, pos=vec(0, -evt.value, 0))

        elif evt.id == "d_theta":
            self.update_position(theta)

        self.calculateMomentOfInertia()

    def update_position(self, theta):
        # self.ang_pos_graph.select()
        self.ang_pos_curve.plot(self.time, theta)
        self.ang_vel_curve.plot(self.time, self.calculate_angular_frequency())
        self.ang_acc_curve.plot(
            self.time, (self.calculate_angular_frequency() - self.prev_ang_freq) / 0.05
        )  # fix this calculation later

        for spoke in self.spokes:
            spoke.rotate(
                angle=-theta,
                axis=vec(0, 0, 1),
                origin=vec(0, 0, 0),
            )

        self.prev_ang_freq = self.calculate_angular_frequency()

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

        without small angle approximation, we also need to consider the vertical displacement of the spring in the spring force. this also makes the force not perindicular to the lever arm.
        """

        total_components = 0
        for spring in self.springs:
            total_components += spring.get_angular_frequency_component().z

        w_squared = abs(total_components / self.momentOfInertia)
        return sqrt(w_squared)

    # def update(self):
    # where the actual simulation goes
    # self.springPoints = points(pos=self.springLocations, color=vec(0, 1, 0))
    # pass
