from vpython import *
from spring import Spring
from wheel import Wheel
from pole import Pole
from constants import SCENE, SPRING_STRETCHED_START_LENGTH


class Simulation:
    def __init__(self):
        self.run = False
        self.previous_theta = 0
        self.small_angle_approx = True
        self.pole = Pole()
        self.spring = Spring(
            length=3 * (SPRING_STRETCHED_START_LENGTH) / 4,
            radius=30,
            spr_wheel_dist=120,
            spr_const=2,
        )  # use single spring for now
        self.spring_arr = [self.spring]

        self.wheel = Wheel(radius=200, mass=15, springs=self.spring_arr)

    def loop(self):
        #print(self.previous_theta)
        theta_amplitude = self.previous_theta
        #print(theta_amplitude)
        time_step = 0
        while (self.run):
            angular_pos = (theta_amplitude * cos(self.angular_frequency * time_step))
            #print(angular_pos)
            delta_theta = angular_pos - self.previous_theta
            self.previous_theta = angular_pos 
        
            self.wheel.update_position(delta_theta)
            for spring in self.spring_arr:
                spring.update_position(delta_theta)  
            sleep(0.05)
            time_step +=1 


    def setup(self):
        SCENE.background = color.white
        self.menu()

        SCENE.center = vec(0, 0, 0)
        SCENE.forward = vec(0, 0, -1)
        SCENE.up = vec(0, 1, 0)
        SCENE.range = 660

        SCENE.userzoom = False
        SCENE.userspin = False
        SCENE.userpan = False

        rate(60)

    def menu(self):
        SCENE.append_to_caption("\n\n")

        ### RUN SIM BUTTON ###
        def bind_run(_):
            self.run = True

        button(bind=bind_run, text="Run Simulation")

        SCENE.append_to_caption("   ")

        ### RESET SIM BUTTON ###
        def bind_reset(_):
            for item in SCENE.objects:
                item.visible = False
                del item

            self.run = False
            self.previous_theta = 0
            self.small_angle_approx = True
            self.pole = Pole()
            self.spring = Spring(
                length=3 * (SPRING_STRETCHED_START_LENGTH) / 4,
                radius=30,
                spr_wheel_dist=120,
                spr_const=2,
            )  # use single spring for now
            self.spring_arr = [self.spring]

            self.wheel = Wheel(radius=200, mass=15, springs=self.spring_arr)

        button(bind=bind_reset, text="Reset Simulation")

        SCENE.append_to_caption("\n\n")

        # SMALL ANGLE APPROX CHECKBOX
        def angle_aprox_bind(evt):
            self.small_angle_approx = evt.checked
            # print(self.small_angle_approx)

        SCENE.append_to_caption("Small Angle Approximation?: ")
        checkbox(bind=angle_aprox_bind, checked=True)

        SCENE.append_to_caption("\n\n")
        ### ANGULAR DISPLACEMENT SLIDER ###

        def d_theta_bind(evt):
            d_theta_text.text = str(evt.value) + " rad\n"

            new_value = evt.value - self.previous_theta
            self.previous_theta = evt.value

            self.spring.change_config(
                evt=evt, wheel_radius=self.wheel.wheel.radius, theta=new_value
            )
            self.wheel.change_config(evt=evt, theta=new_value)

        SCENE.append_to_caption("Angular Displacement: ")
        slider(
            bind=d_theta_bind,
            min=radians(-30),
            value=0,
            max=radians(30),
            step=radians(5),
            length=200,
            id="d_theta",
        )
        d_theta_text = wtext(text="0 rad\n")

        ### MASS SLIDER ###
        def mass_bind(evt):
            mass_text.text = str(evt.value) + " kg\n"
            self.wheel.change_config(evt=evt)  # cleanup in future

        SCENE.append_to_caption("Wheel Mass: ")
        slider(
            bind=mass_bind,
            min=5,
            value=self.wheel.mass,
            max=30,
            step=0.5,
            length=200,
            id="mass",
        )
        mass_text = wtext(text=str(self.wheel.mass) + " kg\n")

        ### WHEEL RADIUS SLIDER ###
        def radius_bind(evt):
            radius_text.text = str(evt.value) + " m\n"
            self.wheel.change_config(evt=evt)  # cleanup in future
            self.spring.change_config(evt=evt, wheel_radius=self.wheel.wheel.radius)

        SCENE.append_to_caption("Wheel Radius: ")
        slider(
            bind=radius_bind,
            min=50,
            value=self.wheel.wheel.radius,
            max=300,
            step=1,
            length=200,
            id="radius",
        )
        radius_text = wtext(text=str(self.wheel.wheel.radius) + " m\n")

        ### SPRING CONSTANT SLIDER ###
        def spr_const_bind(evt):
            spr_const_text.text = str(evt.value) + " N/m\n"
            self.spring.change_config(evt=evt, wheel_radius=self.wheel.wheel.radius)

        SCENE.append_to_caption("Spring Constant: ")
        slider(
            bind=spr_const_bind,
            min=0.5,
            max=5,
            value=self.spring.spr_const,
            step=0.1,
            length=200,
            id="spr_const",
        )
        spr_const_text = wtext(text=str(self.spring.spr_const) + " N/m\n")

        ### SPRING-WHEEL DISTANCE SLIDER ###
        def spr_wheel_dist_bind(evt):
            spr_wheel_dist_text.text = str(evt.value) + " m\n"
            self.spring.change_config(evt=evt, wheel_radius=self.wheel.wheel.radius)

        SCENE.append_to_caption("Spring-Wheel Distance: ")
        slider(
            bind=spr_wheel_dist_bind,
            min=0,
            max=self.wheel.wheel.radius,
            value=self.spring.spring.pos.y,
            step=1,
            length=200,
            id="spr_wheel_dist",
        )
        spr_wheel_dist_text = wtext(text=str(self.spring.spring.pos.y) + " m\n")
