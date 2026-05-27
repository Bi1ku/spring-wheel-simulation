from constants import ROD_X
from constants import SCENE
from vpython import *


class Pole:
    def __init__(self):
        pass

    def display(self):
        curve(
            pos=[
                vec(ROD_X, SCENE.height, 0),
                vec(ROD_X, -SCENE.height, 0),
            ],
            color=color.black,
            radius=10,
        )
