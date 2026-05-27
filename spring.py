from vpython import *
from constants import ROD_X, NUM_SPRINGS


class Spring:
    def __init__(self, length, y_pos, spring_constant):
        self.spring_length = length
        self.spring_position = vector(ROD_X + 50, y_pos, 0)
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
        elif evt.id == "3":
            pass

    def display(self):
        helix(
            pos=self.spring_position,
            axis=vec(1, 0, 0),
            color=color.cyan,
            radius=100,
            length=self.spring_length,
        )
