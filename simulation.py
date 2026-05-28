from vpython import *
from spring import Spring
from wheel import Wheel
from pole import Pole
from constants import SCENE, SPRING_STRETCHED_START_LENGTH


class Simulation:
    def __init__(self):
        self.run = False
        self.previous_theta = 0
        self.small_angle = True
        self.pole = Pole()
        self.spring = Spring(
            length=3 * (SPRING_STRETCHED_START_LENGTH) / 4,
            radius=30,
            spr_wheel_dist=120,
            spr_const=2,
        )  # use single spring for now
        self.spring_arr = [self.spring]

        self.num_springs = 1
        self.wheel = Wheel(radius=200, mass=15, springs=self.spring_arr)

        self.ang_pos_graph = graph(
            title="Angular Position vs Time",
            xtitle="Time (s)",
            ytitle="Angular Position (rad)",
        )
        self.ang_pos_curve = gcurve(color=color.blue)
        self.ang_vel_graph = graph(
            title="Angular Velocity vs Time",
            xtitle="Time (s)",
            ytitle="Angular Velocity (rad/s)",
        )
        self.ang_vel_curve = gcurve(color=color.green)
        self.ang_acc_graph = graph(
            title="Angular Acceleration vs Time",
            xtitle="Time (s)",
            ytitle="Angular Acceleration (rad/s^2)",
        )
        self.ang_acc_curve = gcurve(color=color.orange)


        self.inputs = []

    def loop(self):
        # print(self.previous_theta)
        #print(len(self.inputs))
        for i in range(len(self.inputs)): 
            if i >= 2: # first two is the run and reset simulation buttom
                self.inputs[i].delete()

        if (self.small_angle):
            theta_amplitude = self.previous_theta
            # print(theta_amplitude)
            time_step = 0
            while self.run:
                angular_pos = theta_amplitude * cos(self.angular_frequency * time_step)
                angular_velocity = - theta_amplitude * self.angular_frequency * sin(self.angular_frequency * time_step)
                angular_acceleration = - theta_amplitude * pow(self.angular_frequency, 2) * cos(self.angular_frequency * time_step)
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
            #for input in self.inputs:
                #input.visible = False
            #print(self.previous_theta)
            self.inputs = []

            SCENE.caption = ""
            self.menu()
            if abs(self.spring.spring.pos.y) > abs(self.wheel.wheel.radius):
                if (self.spring.spring.pos.y < 0):
                    self.spring.spring.pos.y = -self.wheel.wheel.radius
                else: 
                    self.spring.spring.pos.y = self.wheel.wheel.radius
            sleep(0.5)

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

            self.ang_pos_graph.delete()
            self.ang_vel_graph.delete()
            self.ang_acc_graph.delete()

            self.run = False

            #self.previous_theta = 0
            #self.small_angle = True
            #self.pole = Pole()
            #self.spring = Spring(
                #length=3 * (SPRING_STRETCHED_START_LENGTH) / 4,
                #radius=30,
                #spr_wheel_dist=120,
                #spr_const=2,
            #)  # use single spring for now
            #self.spring_arr = [self.spring]

            #self.wheel = Wheel(radius=200, mass=15, springs=self.spring_arr)

        self.inputs.append(button(bind=bind_reset, text="Reset Simulation"))

        SCENE.append_to_caption("\n\n")

        # SMALL ANGLE APPROX CHECKBOX
        def angle_aprox_bind(evt):
            self.small_angle = evt.checked
            self.spring.change_config(evt = evt)
            #print("Sim: ")
            #print(self.small_angle)

        SCENE.append_to_caption("Small Angle Approximation?: ")
        self.inputs.append(
            checkbox(
                bind=angle_aprox_bind, 
                checked=self.small_angle, 
                id = "small_angle"
            )
        )

        SCENE.append_to_caption("\n\n")
        ### ANGULAR DISPLACEMENT SLIDER ###

        def d_theta_bind(evt):
            d_theta_text.text = str(evt.value) + " rad\n"

            new_value = evt.value - self.previous_theta
            self.previous_theta = evt.value

            self.spring.change_config(
                evt=evt, theta=new_value
            )
            self.wheel.change_config(evt=evt, theta=new_value)

        SCENE.append_to_caption("Angular Displacement: ")
        self.inputs.append(
            slider(
                bind=d_theta_bind,
                min=radians(-30),
                value=self.previous_theta,
                max=radians(30),
                step=radians(5),
                length=200,
                id="d_theta",
            )
        )
        d_theta_text = wtext(text=str(self.previous_theta) + " rad\n")

        ### MASS SLIDER ###
        def mass_bind(evt):
            mass_text.text = str(evt.value) + " kg\n"
            self.wheel.change_config(evt=evt)  # cleanup in future

        SCENE.append_to_caption("Wheel Mass: ")
        self.inputs.append(
            slider(
                bind=mass_bind,
                min=5,
                value=self.wheel.mass,
                max=30,
                step=0.5,
                length=200,
                id="mass",
            )
        )
        mass_text = wtext(text=str(self.wheel.mass) + " kg\n")

        ### WHEEL RADIUS SLIDER ###
        def radius_bind(evt):
            radius_text.text = str(evt.value) + " m\n"
            self.wheel.change_config(evt=evt)  # cleanup in future
            self.spring.change_config(evt=evt)

        SCENE.append_to_caption("Wheel Radius: ")
        self.inputs.append(
            slider(
                bind=radius_bind,
                min=50,
                value=self.wheel.wheel.radius,
                max=300,
                step=1,
                length=200,
                id="radius",
            )
        )
        radius_text = wtext(text=str(self.wheel.wheel.radius) + " m\n")

        ### SPRING CONSTANT SLIDER ###
        def spr_const_bind(evt):
            spr_const_text.text = str(evt.value) + " N/m\n"
            self.spring.change_config(evt=evt)

        SCENE.append_to_caption("Spring Constant: ")
        self.inputs.append(
            slider(
                bind=spr_const_bind,
                min=0.5,
                max=5,
                value=self.spring.spr_const,
                step=0.1,
                length=200,
                id="spr_const",
            )
        )
        spr_const_text = wtext(text=str(self.spring.spr_const) + " N/m\n")

        ### SPRING-WHEEL DISTANCE SLIDER ###
        def spr_wheel_dist_bind(evt):
            spr_wheel_dist_text.text = str(evt.value) + " m\n"
            self.spring.change_config(evt=evt)

        SCENE.append_to_caption("Spring-Wheel Distance: ")
        self.inputs.append(
            slider(
                bind=spr_wheel_dist_bind,
                min=-self.wheel.wheel.radius,
                max=self.wheel.wheel.radius,
                value=self.spring.spring.pos.y,
                step=1,
                length=200,
                id="spr_wheel_dist",
            )
        )
        spr_wheel_dist_text = wtext(text=str(self.spring.spring.pos.y) + " m\n")

        ### NUMBER OF SPRINGS DROPDOWN ###
        choices = ["1 Spring", "2 Springs", "3 Springs"]

        def num_springs_bind(evt):
            if evt.index == 1:
                self.num_springs = 1
            elif evt.index == 2:
                self.num_springs = 2
            elif evt.index == 3:
                self.num_springs = 3

        SCENE.append_to_caption("Number of Springs: ")
        self.inputs.append(menu(bind=num_springs_bind, choices=choices))