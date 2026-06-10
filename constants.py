from vpython import *

SCENE = canvas(title="Wheel and Spring Simulation", width=800, height=600, align="left")
ROD_X = -scene.width + 50
SPRING_LEFT_X_OFFSET = 12
SPRING_LEFT_X = ROD_X + SPRING_LEFT_X_OFFSET
WHEEL_CENTER_X = 0
WHEEL_CENTER_Y = 0
NUM_SPRINGS = 1
SPRING_STRETCHED_START_LENGTH = WHEEL_CENTER_X - (ROD_X + SPRING_LEFT_X_OFFSET)
