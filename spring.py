from vpython import *
from constants import ROD_X, NUM_SPRINGS


class Spring:
    def __init__(self, length, yPos, springConstant):
        self.springLength = length
        self.leverArm = vector(0, yPos, 0)
        self.equiPosition = vector(ROD_X + 50, yPos, 0)
        self.currentPosition = self.equiPosition
        self.springConstant = springConstant
        
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

    def changePosition(self, position): #not for slider use, must be vector
        self.currentPosition = position

    def changeConstant(self, constant):
        self.springConstant = constant

    def display(self):
        helix(
            pos=self.currentPosition,
            axis=vec(1, 0, 0),
            color=color.cyan,
            radius=100,
            length=self.springLength,
        )
