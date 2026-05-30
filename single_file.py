Web VPython 3.2
from vpython import *

SCENE = canvas(title="Wheel and Spring Simulation", width=800, height=600)
ROD_X = -scene.width + 50
SPRING_LEFT_X_OFFSET = 12
SPRING_LEFT_X = ROD_X + SPRING_LEFT_X_OFFSET
WHEEL_CENTER_X = 0
WHEEL_CENTER_Y = 0
NUM_SPRINGS = 1
SPRING_STRETCHED_START_LENGTH = WHEEL_CENTER_X - (ROD_X + SPRING_LEFT_X_OFFSET)


class Pole:
    def __init__(self):
        curve(pos=[vec(ROD_X, SCENE.height, 0), vec(ROD_X, -SCENE.height, 0)],color=color.black,radius=10,)


class Spring:
    def __init__(self, length, radius, spr_wheel_dist, spr_const, small_angle=True):
        self.spr_const = spr_const
        self.length = length  # natural length
        self.lever_arm_length = abs(spr_wheel_dist)
        self.left_y_level = spr_wheel_dist
        self.lever_arm = vector(0, spr_wheel_dist, 0)
        self.axis = vec(1, 0, 0)  # POSITIVE X
        self.small_angle = small_angle
        # self.arrow = arrow(pos = self.lever_arm, axis = norm(-1 * ((self.spr_const * self.lever_arm_length) * self.axis)) * 100, shaftwidth = 10)

        self.radius = radius

        # Spring length is the strecthed length, not the natural length
        self.spring = helix(pos=vec(SPRING_LEFT_X, self.left_y_level, 0),axis=self.axis,color=color.cyan,radius=radius,length=(SPRING_STRETCHED_START_LENGTH),coils=length / radius)

    def change_config(self, evt, theta=0):
        if evt.id == "spr_const":
            self.spr_const = evt.value
        elif evt.id == "spr_wheel_dist":
            # figure out how to get this to work mid-simulation
            self.spring.pos = vec(SPRING_LEFT_X, evt.value, 0)
        elif evt.id == "d_theta":
            self.update_position(theta)
        elif evt.id == "small_angle":
            self.small_angle = evt.checked
            # print("Spring: ")
            # print(self.small_angle)

    def update_position(self, theta):
        if self.small_angle:
            self.spring.length += theta * self.lever_arm_length
            self.lever_arm = rotate(self.lever_arm, angle=-theta, axis=vector(0, 0, 1))
            # self.arrow.visible = False
            # if self.spring.length < self.length:
            #     self.arrow = arrow(pos = self.lever_arm, axis = norm((self.spr_const * self.lever_arm_length) * self.axis) * 100, shaftwidth = 10)
            # elif self.spring.length > self.length:
            #     self.arrow = arrow(pos = self.lever_arm, axis = norm(-1 * ((self.spr_const * self.lever_arm_length) * self.axis)) * 100, shaftwidth = 10)
            # self.spring.visible = False
            # self.spring = helix(
            #     pos=vec(0, 0, 0),
            #     axis=self.lever_arm,
            #     color=color.cyan,
            #     radius=self.radius,
            #     length=(self.left_y_level),
            #     coils=self.length / self.radius,
            # )
        else:
            self.lever_arm = rotate(self.lever_arm, angle=-theta, axis=vector(0, 0, 1))
            self.axis = self.lever_arm - self.spring.pos
            self.spring.visible = False
            self.spring = helix(pos=vec(SPRING_LEFT_X, self.left_y_level, 0),axis=self.axis,color=color.cyan,radius=self.radius,length=(mag(self.axis)),coils=self.length / self.radius)
            # print(self.spring.length - self.length)
            # self.arrow = arrow(pos = self.lever_arm, axis = norm(-1 * ((self.spr_const * (self.spring.length - self.length)) * self.axis)) * 100, shaftwidth = 10)

    def get_angular_frequency_component(self):
        if self.spring.length < self.length:
            return cross((self.spr_const * self.lever_arm_length) * self.axis, self.lever_arm)
        elif self.spring.length > self.length:
            return cross(-1 * ((self.spr_const * self.lever_arm_length) * self.axis),self.lever_arm)
        else:
            return vec(0, 0, 0)

    def get_torque(self):
        return cross(-1 * ((self.spr_const * (self.spring.length - self.length)) * self.axis),self.lever_arm)
        pass

    # def update(self):
    # where actual simulation goes
    # pass


class Wheel:
    def __init__(self, radius, mass, springs):
        self.springs = springs
        self.mass = mass
        self.time = 0.0

        self.wheel = cylinder(pos=vec(WHEEL_CENTER_X, WHEEL_CENTER_Y, 0), axis=vec(WHEEL_CENTER_X, WHEEL_CENTER_Y, -1),radius=radius,length=1,color=color.red,opacity=0.5,make_trail=True)

        spoke1 = curve(pos=[vec(0, 0, 0), vec(radius, 0, 0)],color=color.black,radius=5)

        spoke2 = curve(pos=[vec(0, 0, 0), vec(0, radius, 0)],color=color.black,radius=5)

        spoke3 = curve(pos=[vec(0, 0, 0), vec(-radius, 0, 0)],color=color.black,radius=5)

        spoke4 = curve(pos=[vec(0, 0, 0), vec(0, -radius, 0)],color=color.black,radius=5)

        self.spokes = [spoke1, spoke2, spoke3, spoke4]

        # self.springPoints = points(pos=self.springs, color=vec(0, 1, 0))

        self.calculateMomentOfInertia()

    def calculateMomentOfInertia(self):
        self.momentOfInertia = 0.5 * self.mass * pow(self.wheel.radius, 2)

    def change_config(self, evt, theta=0):
        if evt.id == "mass":
            self.mass = evt.value

        elif evt.id == "radius":
            self.wheel.radius = evt.value
            self.spokes[0].modify(1, pos=vec(evt.value, 0, 0))
            self.spokes[1].modify(1, pos=vec(0, evt.value, 0))
            self.spokes[2].modify(1, pos=vec(-evt.value, 0, 0))
            self.spokes[3].modify(1, pos=vec(0, -evt.value, 0))

        elif evt.id == "d_theta":
            self.update_position(theta)

        self.calculateMomentOfInertia()

    def update_position(self, theta):
        for spoke in self.spokes:
            spoke.rotate(angle=-theta,axis=vec(0, 0, 1),origin=vec(0, 0, 0))

    def calculate_angular_frequency(self):
        """
        let me cook here
        t = torque
        a = angular acceleration
        l = lever arm for spring

        t = I * a
        -k(l * theta) x l = 0.5 * m * r^2 * a
        (-k*l^2)/(0.5 * m*r^2) * theta = a
        so we only need to get the sum of all -k * l^2 (still need to consider them as vectors) to calculate angular frequency
        """

        total_components = 0
        for spring in self.springs:
            total_components += spring.get_angular_frequency_component().z

        w_squared = abs(total_components / self.momentOfInertia)
        return sqrt(w_squared)

    # def update(self):
    # where the actual simulation goes
    # self.springPoints = points(pos=self.springLocations, color=vec(0, 1, 0))
    # pass


class Simulation:
    def __init__(self):
        self.run = False
        self.pause = False
        self.previous_theta = 0
        self.small_angle = True
        self.pole = Pole()
        self.spring = Spring(length=3 * (SPRING_STRETCHED_START_LENGTH) / 4,radius=30,spr_wheel_dist=120,spr_const=2)  # use single spring for now
        self.spring_arr = [self.spring]

        self.num_springs = 1
        self.wheel = Wheel(radius=200, mass=15, springs=self.spring_arr)

        self.ang_pos_graph = graph(title="Angular Position vs Time",xtitle="Time (s)",ytitle="Angular Position (rad)")
        self.ang_pos_curve = gcurve(color=color.blue)
        self.ang_vel_graph = graph(title="Angular Velocity vs Time",xtitle="Time (s)",ytitle="Angular Velocity (rad/s)")
        self.ang_vel_curve = gcurve(color=color.green)
        self.ang_acc_graph = graph(title="Angular Acceleration vs Time",xtitle="Time (s)",ytitle="Angular Acceleration (rad/s^2)")
        self.ang_acc_curve = gcurve(color=color.orange)

        self.inputs = []

    def loop(self):
        # print(self.previous_theta)
        # print(len(self.inputs))
        for i in range(len(self.inputs)):
            if i >= 3:  # first three is the run, reset, pause simulation buttons
                self.inputs[i].delete()

        if self.small_angle:
            theta_amplitude = self.previous_theta
            # print(theta_amplitude)
            time_step = 0
            while self.run:
                while self.pause:
                    sleep(0.5)
                angular_pos = theta_amplitude * cos(self.angular_frequency * time_step)
                angular_velocity = (-theta_amplitude* self.angular_frequency* sin(self.angular_frequency * time_step))
                angular_acceleration = (-theta_amplitude* pow(self.angular_frequency, 2)* cos(self.angular_frequency * time_step))
                # print(angular_pos)
                delta_theta = angular_pos - self.previous_theta
                self.previous_theta = angular_pos

                self.wheel.update_position(delta_theta)
                for spring in self.spring_arr:
                    spring.update_position(delta_theta)

                # self.ang_pos_graph.select()
                self.ang_pos_curve.plot(time_step, angular_pos)
                self.ang_vel_curve.plot(time_step, angular_velocity)
                self.ang_acc_curve.plot(time_step, angular_acceleration)  # fix this calculation later

                sleep(0.05)
                self.wheel.time += 0.05
                time_step += 1
        else:
            pass

    def setup(self):
        SCENE.background = color.white

        SCENE.center = vec(0, 0, 0)
        SCENE.forward = vec(0, 0, -1)
        SCENE.up = vec(0, 1, 0)
        SCENE.range = 660

        SCENE.userzoom = False
        SCENE.userspin = False
        SCENE.userpan = False

        self.angular_frequency = self.wheel.calculate_angular_frequency()
    
        while not self.run:
            for input in self.inputs:
                input.visible = False
                input.delete()
                self.inputs.remove(input)

            SCENE.caption = ""
            self.menu()
            if abs(self.spring.spring.pos.y) > abs(self.wheel.wheel.radius):
                if self.spring.spring.pos.y < 0:
                    self.spring.spring.pos.y = -self.wheel.wheel.radius
                else:
                    self.spring.spring.pos.y = self.wheel.wheel.radius
            sleep(1)

    def menu(self):
        SCENE.append_to_caption("\n\n")

        ### RUN SIM BUTTON ### IMPORTANT: MUST BE FIRST OR SECOND IN INPUTS LIST!!!!!
        def bind_run(_):
            self.run = True

        self.inputs.append(button(bind=bind_run, text="Run Simulation"))

        SCENE.append_to_caption("   ")

        ### RESET SIM BUTTON ### IMPORTANT: MUST BE FIRST OR SECOND IN INPUTS LIST!!!!!
        def bind_reset(_):
            for item in SCENE.objects:
                item.visible = False
                del item

            self.run = False
            self.pause = False
            self.previous_theta = 0
            self.small_angle_approx = True
            self.pole = Pole()
            self.spring = Spring(length=3 * (SPRING_STRETCHED_START_LENGTH) / 4,radius=30,spr_wheel_dist=120,spr_const=2)  # use single spring for now
            self.spring_arr = [self.spring]

            self.ang_pos_graph.delete()
            self.ang_vel_graph.delete()
            self.ang_acc_graph.delete()
            self.wheel = Wheel(radius=200, mass=15, springs=self.spring_arr)

        self.inputs.append(button(bind=bind_reset, text="Reset Simulation"))
        SCENE.append_to_caption("   ")

        ## PAUSE SIM BUTTON ###
        def bind_pause(_):
            self.pause = not self.pause

        self.inputs.append(button(bind=bind_pause, text="Pause/Unpause Simulation"))

        SCENE.append_to_caption("\n\n")

        # SMALL ANGLE APPROX CHECKBOX
        def angle_aprox_bind(evt):
            self.small_angle = evt.checked
            self.spring.change_config(evt=evt)
            # print("Sim: ")
            # print(self.small_angle)

        SCENE.append_to_caption("Small Angle Approximation?: ")
        self.inputs.append(checkbox(bind=angle_aprox_bind, checked=self.small_angle, id="small_angle"))

        SCENE.append_to_caption("\n\n")
        ### ANGULAR DISPLACEMENT SLIDER ###

        def d_theta_bind(evt):
            d_theta_text.text = str(evt.value) + " rad\n"

            new_value = evt.value - self.previous_theta
            self.previous_theta = evt.value

            self.spring.change_config(evt=evt, theta=new_value)
            self.wheel.change_config(evt=evt, theta=new_value)

        SCENE.append_to_caption("Angular Displacement: ")
        self.inputs.append(slider(bind=d_theta_bind,min=radians(-30) if self.small_angle else radians(-180),value=self.previous_theta,max=radians(30) if self.small_angle else radians(180),step=radians(5),length=200,id="d_theta"))
        d_theta_text = wtext(text=str(self.previous_theta) + " rad\n")

        ### MASS SLIDER ###
        def mass_bind(evt):
            mass_text.text = str(evt.value) + " kg\n"
            self.wheel.change_config(evt=evt)  # cleanup in future

        SCENE.append_to_caption("Wheel Mass: ")
        self.inputs.append(slider(bind=mass_bind,min=5,value=self.wheel.mass,max=30,step=0.5,length=200,id="mass"))
        mass_text = wtext(text=str(self.wheel.mass) + " kg\n")

        ### WHEEL RADIUS SLIDER ###
        def radius_bind(evt):
            radius_text.text = str(evt.value) + " m\n"
            self.wheel.change_config(evt=evt)  # cleanup in future
            self.spring.change_config(evt=evt)

        SCENE.append_to_caption("Wheel Radius: ")
        self.inputs.append(slider(bind=radius_bind,min=50,value=self.wheel.wheel.radius,max=300,step=1,length=200,id="radius"))
        radius_text = wtext(text=str(self.wheel.wheel.radius) + " m\n")

        ### SPRING CONSTANT SLIDER ###
        def spr_const_bind(evt):
            spr_const_text.text = str(evt.value) + " N/m\n"
            self.spring.change_config(evt=evt)

        SCENE.append_to_caption("Spring Constant: ")
        self.inputs.append(slider(bind=spr_const_bind,min=0.5,max=5,value=self.spring.spr_const,step=0.1,length=200,id="spr_const"))
        spr_const_text = wtext(text=str(self.spring.spr_const) + " N/m\n")

        ### SPRING-WHEEL DISTANCE SLIDER ###
        def spr_wheel_dist_bind(evt):
            spr_wheel_dist_text.text = str(evt.value) + " m\n"
            self.spring.change_config(evt=evt)

        SCENE.append_to_caption("Spring-Wheel Distance: ")
        self.inputs.append(slider(bind=spr_wheel_dist_bind,min=-self.wheel.wheel.radius,max=self.wheel.wheel.radius,value=self.spring.spring.pos.y,step=1,length=200,id="spr_wheel_dist"))
        spr_wheel_dist_text = wtext(text=str(self.spring.spring.pos.y) + " m\n")


if __name__ == "__main__":
    simulation = Simulation()
    while True:
        simulation.setup()

        run = False
        while not run:
            run = simulation.run

        if run:
            simulation.loop()
