from vpython import *
from constants import ROD_X


class Spring:
    def __init__(self, length, radius, y_pos, spr_const):
        self.spr_const = spr_const
        self.length = length

        # Spring length is the strecthed length, not the natural length
        self.spring = helix(
            pos=vec(ROD_X + 12, y_pos, 0),
            axis=vec(1, 0, 0),
            color=color.cyan,
            radius=radius,
            length=length,
            coils=length / radius,
        )

    def changePosition(self, position):  # not for slider use, must be vector
        self.currentPosition = position

    def changeConstant(self, constant):
        self.springConstant = constant

    def update(self, d_theta, wheel_radius):
        self.spring.length = self.length + d_theta * wheel_radius
