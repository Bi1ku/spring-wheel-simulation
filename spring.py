from vpython import *
from constants import ROD_X, SPRING_LEFT_X_OFFSET


class Spring:
    def __init__(self, length, radius, spr_wheel_dist, spr_const):
        self.spr_const = spr_const
        self.length = length

        # Spring length is the strecthed length, not the natural length
        self.spring = helix(
            pos=vec(ROD_X + SPRING_LEFT_X_OFFSET, spr_wheel_dist, 0),
            axis=vec(1, 0, 0),
            color=color.cyan,
            radius=radius,
            length=length,
            coils=length / radius,
        )

    def change_config(self, evt, wheel_radius):
        if evt.id == "spr_const":
            self.spr_const = evt.value
        elif evt.id == "spr_wheel_dist":
            self.spring.pos = vec(ROD_X + SPRING_LEFT_X_OFFSET, evt.value, 0)
        elif evt.id == "d_theta":
            self.spring.length = self.length + evt.value * wheel_radius

    def update(self):
        # where actual simulation goes
        pass
