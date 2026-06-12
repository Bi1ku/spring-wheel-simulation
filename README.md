### Spring Wheel System Simulation

Our project's main purpose is to simulate the physics of a spring-wheel system. The spring(s) are attached to a
stationary pole at a certain natural length, x-axis displacement from the wheel, and y-axis displacement from the 
wheel, values that are all able to be changed by the user. The wheel is being rotated about its center of mass from
a position to the right of the pole. The number of springs is also modifiable with a limit of three.

There are also many properties of the wheel that you can change! These fields include its mass and radius. Another
important feature we implemented was the ability to make your own custom object/"wheel". The custom object can be 
any shape, which the user can specify by plotting vertices directly on the canvas.

Graphs for angular position, angular velocity, and angular acceleration will all be dynamically plotted and visible
after the simulation is ran. The user will also have the choice to enable (or disable) the use of small angle
approximations in our math for the simulation! We found it really interesting to compare the graphical differences 
between the two calculations.

### New Physics

Though the core of our project is primarily derived from our work in class with simple harmonic oscillators, angular
kinematics, and springs, there are also some interesting new factors/parts we had to consider. Our main challenge
was figuring out the logic for the aforementioned disabling of small angle approximations.

Without the use of small angle approximations, (...)

To calculate inertias for the irregular 2D shape given a list of vertices, we did some research online, focusing 
particularly on the Shoelace Theorem and its collararies. Since we assume uniform density, we can just focus on areas
(which can be calculated with shoelace). The center of mass of the shape is just the centroid, which is a arbitrary 
summation multiplied by 1/6 times the area. There are also collararies to find the second moment of inertia about
the x-axis and y-axis, which we can then manipulate to find the moment of inertia about the center of mass using
the Parallel Axis Theorem. If you're still interested about the math, please view our code in wheel.py!

### Running the Program

(...)
