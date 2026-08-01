# SpringForge

An interactive physics simulator for exploring the rotational motion of configurable spring-wheel systems and custom 2D shapes.

## Overview

SpringForge was built as an AP Physics C final project to visualize how springs create torque on a rotating object. It supports both the small-angle approximation and a nonlinear model, making it easy to compare simplified harmonic motion with a more complete physics simulation.

## Key Features

* Configure systems with one to three springs
* Adjust wheel mass, radius, spring constants, natural lengths, and attachment positions
* Set the initial angular displacement
* Enable or disable the small-angle approximation
* Draw custom polygonal objects directly in the simulation
* Calculate the center of mass and moment of inertia of custom shapes
* Move a custom object's center of mass to the axis of rotation
* Dynamically graph angular position, velocity, and acceleration
* Pause, resume, and reset the simulation

## Tech Stack

* **Python**
* **VPython**
* Computational geometry using the shoelace formula and parallel-axis theorem
* Numerical integration for nonlinear rotational motion

## Installation

Clone the repository:

```bash
git clone https://github.com/Bi1ku/SpringForge.git
cd SpringForge
```

Install VPython:

```bash
python -m pip install vpython
```

## Usage

Start the simulation with:

```bash
python main.py
```

Inside the simulation:

1. Choose whether to use the small-angle approximation.
2. Configure the wheel and springs using the provided controls.
3. Optionally draw a custom object by plotting at least three points.
4. Set the initial angular displacement.
5. Run the simulation and view the resulting motion and graphs.
