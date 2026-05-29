from vpython import *
from constants import (
    ROD_X,
    SPRING_LEFT_X,
    SPRING_STRETCHED_START_LENGTH,
    SPRING_LEFT_X_OFFSET,
)


class Spring:
    def __init__(self, length, radius, spr_wheel_dist, spr_const, small_angle = True):
        self.spr_const = spr_const
        self.length = length  # natural length
        self.lever_arm_length = abs(spr_wheel_dist)
        self.left_y_level = spr_wheel_dist
        self.lever_arm = vector(0, spr_wheel_dist, 0)
        self.axis = vec(1, 0, 0)  # POSITIVE X
        self.small_angle = small_angle
        #self.arrow = arrow(pos = self.lever_arm, axis = norm(-1 * ((self.spr_const * self.lever_arm_length) * self.axis)) * 100, shaftwidth = 10)

        self.radius = radius

        # Spring length is the strecthed length, not the natural length
        self.spring = helix(
            pos=vec(SPRING_LEFT_X, self.left_y_level, 0),
            axis=self.axis,
            color=color.cyan,
            radius=radius,
            length=(SPRING_STRETCHED_START_LENGTH),
            coils=length / radius,
        )

    def change_config(self, evt, theta=0):
        if evt.id == "spr_const":
            self.spr_const = evt.value
        elif evt.id == "spr_wheel_dist":
            # figure out how to get this to work mid-simulation
            self.spring.pos = vec(SPRING_LEFT_X, evt.value, 0)
        elif evt.id == "d_theta":
            self.update_position(theta)
        elif evt.id == "small_angle":
            self.small_angle = evt.checked
            #print("Spring: ")
            #print(self.small_angle)

    def update_position(self, theta):
        if self.small_angle: 
            self.spring.length += theta * self.lever_arm_length
            self.lever_arm = rotate(self.lever_arm, angle=-theta, axis=vector(0, 0, 1))
            # self.arrow.visible = False
            # if self.spring.length < self.length:
            #     self.arrow = arrow(pos = self.lever_arm, axis = norm((self.spr_const * self.lever_arm_length) * self.axis) * 100, shaftwidth = 10)
            # elif self.spring.length > self.length: 
            #     self.arrow = arrow(pos = self.lever_arm, axis = norm(-1 * ((self.spr_const * self.lever_arm_length) * self.axis)) * 100, shaftwidth = 10)
            # self.spring.visible = False
            # self.spring = helix(
            #     pos=vec(0, 0, 0),
            #     axis=self.lever_arm,
            #     color=color.cyan,
            #     radius=self.radius,
            #     length=(self.left_y_level),
            #     coils=self.length / self.radius,
            # )
        else: 
            self.lever_arm = rotate(self.lever_arm, angle=-theta, axis=vector(0, 0, 1))
            self.axis = (self.lever_arm - self.spring.pos)
            self.spring.visible = False
            self.spring = helix(
                pos=vec(SPRING_LEFT_X, self.left_y_level, 0),
                axis=self.axis,
                color=color.cyan,
                radius=self.radius,
                length=(mag(self.axis)),
                coils=self.length / self.radius,
            )
            #print(self.spring.length - self.length)
            #self.arrow = arrow(pos = self.lever_arm, axis = norm(-1 * ((self.spr_const * (self.spring.length - self.length)) * self.axis)) * 100, shaftwidth = 10)

    def get_angular_frequency_component(self):
        if self.spring.length < self.length:
            return cross(
                (self.spr_const * self.lever_arm_length) * self.axis, 
                self.lever_arm 
            )
        elif self.spring.length > self.length:
            return cross(
                -1 * ((self.spr_const * self.lever_arm_length) * self.axis), 
                self.lever_arm 
            )
        else:
            return vec(0,0,0)

    def get_torque(self):
        return cross(
            -1 * ((self.spr_const * (self.spring.length - self.length)) * self.axis), 
            self.lever_arm 
        ) 

    #def update(self):
        # where actual simulation goes
       # pass
