### Spring Wheel System Simulation

Our project's main purpose is to simulate the physics of a spring-wheel system. The spring(s) are attached to a
stationary pole at a certain natural length, x-axis displacement from the wheel (only if small angle approximation is 
not being used), and y-axis displacement from the wheel, values that are all able to be changed by the user. The wheel is 
being rotated about its center of mass from a position to the right of the pole. The number of springs is also modifiable
with a limit of three.

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

Without the use of small angle approximations, we can't assume simple harmonic motion since angular acceleration is now
no longer directly related ot theta, but rather sin(theta). We also cannot use the convenient fact that
x = r * theta to update the position of the spring. We therefore had to make sure the end of the spring attached to the 
wheel traveled exactly with wheel, updating the vector for lever arm for every tick of the simulation so that the torque 
calculation is correct. 

### Running the Program 

First, the user must choose whether or not they want to use small angle approximation for the simulation of the wheel. 
Note that when making a custom object, small angle approximation will be set to false always regardless of the user's
initial input. This is done because the combination small angle approximation and certain custom objects causes the springs
attached to the wheel to extend way past the object. We therefore removed this option entirely because it looks a little too
ridiculous. 

After setting the small angle approximation, the user can set the various fields mentioned above, like the mass of the
wheel/custom object, the radius of only the wheel, the number of springs, the spring constant for each spring, and the initial 
displacement from the axis of rotation of each spring. After finishing the inputs, the user can then set the initial angular
displacement of the wheel-springs system and, finally, run the simulation!

To create your own custom object, you can click the Draw Custom Object button that's available at the same time you are setting 
the inputs above (mass, num springs, etc). You must click and add at least 3 points on the canvas to be able to finish drawing. 
Once you have added at least 3 points, you can press the Finish Custom Object button. At any time, you can remove the last point you've
added, or completely stop drawing and remove every point that you've drawn.
