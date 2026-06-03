from vpython import *

from spring import Spring
from wheel import Wheel
from pole import Pole
from constants import SCENE, SPRING_STRETCHED_START_LENGTH


class Simulation:
    def __init__(self):
        self.run = False
        self.pause = False
        self.previous_theta = 0
        self.small_angle = True
        self.small_angle_disabled = False
        self.draw = False
        self.custom_object = False
        self.pole = Pole()
        self.spring_arr = [Spring(length=3 * (SPRING_STRETCHED_START_LENGTH) / 4,radius=30,spr_wheel_dist=120,spr_const=2)]
        self.custom_points = []

        self.num_springs = 1
        self.wheel = Wheel(radius=200, mass=15, springs=self.spring_arr)

        self.ang_pos_graph = graph(title="Angular Position vs Time",xtitle="Time (s)",ytitle="Angular Position (rad)")
        self.ang_pos_curve = gcurve(color=color.blue)
        self.ang_vel_graph = graph(title="Angular Velocity vs Time",xtitle="Time (s)",ytitle="Angular Velocity (rad/s)")
        self.ang_vel_curve = gcurve(color=color.green)
        self.ang_acc_graph = graph(title="Angular Acceleration vs Time",xtitle="Time (s)",ytitle="Angular Acceleration (rad/s^2)")
        self.ang_acc_curve = gcurve(color=color.orange)

        self.inputs = []
        self.spr_wheel_dist_texts = []
        self.spr_const_texts = []

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
            angular_vel = 0;
            angular_pos = 0; 
            time_step = 0
            delta_time_step = 0.05
            while self.run:
                while self.pause:
                    sleep(0.5)
               
                angular_accel = self.wheel.calculate_angular_accel() 
                angular_vel += angular_accel * delta_time_step
                angular_disp = angular_vel * delta_time_step
                angular_pos += angular_disp
                #print(angular_accel)

                self.wheel.update_position(angular_disp)
                for spring in self.spring_arr:
                    spring.update_position(angular_disp)
                
                self.ang_pos_curve.plot(time_step, angular_pos)
                self.ang_vel_curve.plot(time_step, angular_vel)
                self.ang_acc_curve.plot(time_step, angular_accel)
                
                sleep(0.1)
                self.wheel.time += 0.05
                time_step += delta_time_step
               

    def add_custom_point(self):
        if self.draw and (self.custom_points == [] or vec(self.custom_points[-1].pos.x, self.custom_points[-1].pos.y, 0) != SCENE.mouse.pos):
            print(self.draw)
            self.custom_points.append(sphere(pos=SCENE.mouse.pos, radius=12.5, color=color.black))
            print(SCENE.mouse.pos)

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
            if self.draw:
                SCENE.bind('click', self.add_custom_point)
            
            # for input in self.inputs:
            # input.visible = False
            # print(self.previous_theta)
            self.inputs = []
            for spring in self.spring_arr:
                # print(spring.spring.pos.y)
                pass

            SCENE.caption = ""
            self.menu()
            for spring in self.spring_arr:
                if abs(spring.spring.pos.y) > abs(self.wheel.wheel.radius):
                    if spring.spring.pos.y < 0:
                        spring.spring.pos.y = -self.wheel.wheel.radius
                    else:
                        spring.spring.pos.y = self.wheel.wheel.radius
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
            self.custom_points = []
            self.custom_object = False
            self.draw = False
            self.previous_theta = 0
            self.small_angle = True
            self.small_angle_disabled = False
            self.draw = False
            self.pole = Pole()
            self.spring_arr = [Spring(length=3 * (SPRING_STRETCHED_START_LENGTH) / 4,radius=30,spr_wheel_dist=120,spr_const=2)]  # use single spring for now

            self.ang_pos_graph.delete()
            self.ang_vel_graph.delete()
            self.ang_acc_graph.delete()
            self.wheel = Wheel(radius=200, mass=15, springs=self.spring_arr)

            self.ang_pos_graph = graph(title="Angular Position vs Time",xtitle="Time (s)",ytitle="Angular Position (rad)")
            self.ang_pos_curve = gcurve(color=color.blue)
            self.ang_vel_graph = graph(title="Angular Velocity vs Time",xtitle="Time (s)",ytitle="Angular Velocity (rad/s)")
            self.ang_vel_curve = gcurve(color=color.green)
            self.ang_acc_graph = graph(title="Angular Acceleration vs Time",xtitle="Time (s)",ytitle="Angular Acceleration (rad/s^2)")
            self.ang_acc_curve = gcurve(color=color.orange)

        self.inputs.append(button(bind=bind_reset, text="Reset Simulation"))
        SCENE.append_to_caption("   ")

        ## PAUSE SIM BUTTON ###
        def bind_pause(_):
            self.pause = not self.pause

        self.inputs.append(button(bind=bind_pause, text="Pause/Unpause Simulation"))
        
        SCENE.append_to_caption("\n\n")

        ## DRAW OBJECT BUTTON ###
        if not (self.draw or self.custom_object):
            def bind_draw(_):
                self.draw = True

            self.inputs.append(button(bind=bind_draw, text="Draw Custom Object")) 
            SCENE.append_to_caption("   ")

        ### DRAW FINISH BUTTON ###
        def bind_draw_finish(_):
            if len(self.custom_points) < 3:
                pass # do nothing if you can't create closed object
                print("can't finish object")
            else:
                self.custom_object = True
                two_d_points = []
                for point in self.custom_points:
                    two_d_points.append([point.pos.x, point.pos.y])
                    point.visible = False

                self.wheel.wheel.visible = False
                for spoke in self.wheel.spokes:
                    spoke.visible = False

                shape = shapes.points(pos=two_d_points)
                extrude = extrusion(path=[vec(0, 0, 0), vec(0, 0, -1)], shape=shape, color=color.red)
                self.wheel.points = two_d_points
                self.wheel.add_extrusion(extrude)
                self.draw = False
        
        if self.draw:
            self.inputs.append(button(bind=bind_draw_finish, text="Finish Custom Object"))

        if not self.custom_object:
            SCENE.append_to_caption("   ")
        ### DRAW UNDO BUTTON ###
        def bind_draw_undo(_):
            if len(self.custom_points) > 0:
                self.custom_points[-1].visible = False
                self.custom_points[-1].delete()
                self.custom_points.pop()

            #print("test")
        
        if self.draw:
            self.inputs.append(button(bind=bind_draw_undo, text="Undo Last Point"))


        if not self.custom_object:
            SCENE.append_to_caption("   ")
        ### STOP DRAW BUTTON ###
        def bind_draw_stop(_):
                self.draw = False
                self.custom_object = False
                for point in self.custom_points:
                    point.visible = False
                self.custom_points = []
       
        if self.draw:
            self.inputs.append(button(bind=bind_draw_stop, text="Stop Drawing"))
 
        if not self.custom_object:
            SCENE.append_to_caption("\n\n")
        # SMALL ANGLE APPROX CHECKBOX
        def angle_aprox_bind(evt):
            self.small_angle = evt.checked
            for spring in self.spring_arr:
                spring.change_config(evt=evt)
            self.small_angle_disabled = True
            # print("Sim: ")
            # print(self.small_angle)

        SCENE.append_to_caption("Small Angle Approximation?: ")
        self.small_angle_checkbox = checkbox(bind=angle_aprox_bind, checked=self.small_angle, id="small_angle")
        self.inputs.append(self.small_angle_checkbox);

        self.small_angle_checkbox.disabled = self.small_angle_disabled # disabling checkbox

        SCENE.append_to_caption("\n\n") 

        ### ANGULAR DISPLACEMENT SLIDER ###

        def d_theta_bind(evt):
            d_theta_text.text = str(evt.value) + " rad\n"

            new_value = evt.value - self.previous_theta
            self.previous_theta = evt.value

            for spring in self.spring_arr:
                spring.change_config(evt=evt, theta=new_value)

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
        if not (self.draw or self.custom_object):
            def radius_bind(evt):
                radius_text.text = str(evt.value) + " m\n"
                self.wheel.change_config(evt=evt)  # cleanup in future
                for spring in self.spring_arr:
                    spring.change_config(evt=evt)
    
            SCENE.append_to_caption("Wheel Radius: ")
            self.inputs.append(slider(bind=radius_bind,min=50,value=self.wheel.wheel.radius,max=300,step=1,length=200,id="radius"))
            radius_text = wtext(text=str(self.wheel.wheel.radius) + " m\n")

        ### NUMBER OF SPRINGS DROPDOWN ###
        def num_springs_bind(evt):
            if evt.value > len(self.spring_arr):
                self.spring_arr.append(Spring(length=3 * (SPRING_STRETCHED_START_LENGTH) / 4,radius=30,spr_wheel_dist=evt.value,spr_const=2,small_angle = self.small_angle))
            elif evt.value < len(self.spring_arr):
                self.spring_arr[-1].spring.visible = False
                self.spring_arr[-1].spring.delete()
                self.spring_arr.pop()

            num_springs_text.text = str(evt.value) + " springs \n"

        SCENE.append_to_caption("Number of Springs: ")
        self.inputs.append(slider(bind=num_springs_bind,min=1,max=3,value=len(self.spring_arr),step=1,length=200))
        num_springs_text = wtext(text=str(len(self.spring_arr)) + " springs \n")
        SCENE.append_to_caption("\n")

        ### SPRING CONSTANT SLIDER ###
        def spr_const_bind(evt):
            self.spr_const_texts[int(evt.id[-1])].text = str(evt.value) + " N/m\n"
            for i in range(len(self.spring_arr)):
                self.spring_arr[i].change_config(evt=evt, num=i + 1)

        for i in range(len(self.spring_arr)):
            SCENE.append_to_caption(f"Spring {i + 1} Constant: ")
            self.inputs.append(slider(bind=spr_const_bind,min=0.5,max=5,value=self.spring_arr[i].spr_const,step=0.1,length=200,id=f"spr_const_{i + 1}"))
            self.spr_const_texts.append(wtext(text=str(self.spring_arr[i].spr_const) + " N/m\n"))

        ### SPRING-WHEEL DISTANCE SLIDER ###
        def spr_wheel_dist_bind(evt):
            self.spr_wheel_dist_texts[int(evt.id[-1]) - 1].text = (str(evt.value) + " m\n")
            for i in range(len(self.spring_arr)):
                self.spring_arr[i].change_config(evt=evt, num=i + 1)

        for i in range(len(self.spring_arr)):
            SCENE.append_to_caption(f"Spring {i + 1}-Wheel Distance:")
            self.inputs.append(slider(bind=spr_wheel_dist_bind,min=-self.wheel.wheel.radius,max=self.wheel.wheel.radius,value=self.spring_arr[i].spring.pos.y,step=1,length=200,id=f"spr_wheel_dist_{i + 1}"))
            self.spr_wheel_dist_texts.append(wtext(text=str(self.spring_arr[i].spring.pos.y) + " m\n"))

        SCENE.append_to_caption("\n\n\n\n\n\n\n")
