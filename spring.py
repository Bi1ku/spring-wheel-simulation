from vpython import *
from constants import SPRING_LEFT_X, SPRING_STRETCHED_START_LENGTH


class Spring:
    def __init__(self, length, radius, spr_wheel_dist, spr_const):
        self.spr_const = spr_const
        self.length = length #natural length
        self.lever_arm_length = spr_wheel_dist
        self.lever_arm = vector(0, spr_wheel_dist, 0)
        self.axis = vec(1,0,0) # POSITIVE X
        # Spring length is the strecthed length, not the natural length
        self.spring = helix(
            pos=vec(SPRING_LEFT_X, spr_wheel_dist, 0),
            axis=self.axis,
            color=color.cyan,
            radius=radius,
            length=(SPRING_STRETCHED_START_LENGTH), 
            coils=length / radius,
        )

    def change_config(self, evt, wheel_radius, theta = 0):
        if evt.id == "spr_const":
            self.spr_const = evt.value
        elif evt.id == "spr_wheel_dist":
            self.spring.pos = vec(ROD_X + SPRING_LEFT_X_OFFSET, evt.value, 0) # figure out how to get this to work mid-simulation
        elif evt.id == "d_theta":
            self.update_position(theta, wheel_radius)

    def update_position(self, theta):
        self.spring.length += theta * self.lever_arm_length
        self.lever_arm = rotate(self.lever_arm, angle = theta, axis = vector(0, 0, 1))

    def get_angular_frequency_component(self):

        if self.spring.length < self.length:
            return cross(
                (k * spr_wheel_dist) * self.axis, 
                self.lever_arm 
            )
        elif self.spring.length > self.length:
            return cross(
                (-k * spr_wheel_dist) * self.axis, 
                self.lever_arm 
            )
        else:
            return 0

    def update(self):
        # where actual simulation goes
        pass
