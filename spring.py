from vpython import *
from constants import ROD_X, NUM_SPRINGS


class Spring:
    def __init__(self, length, radius, y_pos, spring_constant):
        self.radius = radius
        self.length = length
        self.pos = vector(ROD_X + 35, y_pos, 0)
        self.constant = spring_constant

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
        elif evt.id == "3":
            pass

    def display(self):
        helix(
            pos=self.pos,
            axis=vec(1, 0, 0),
            color=color.cyan,
            radius=self.radius,
            length=self.length,
        )

    def update(self):
        pass
