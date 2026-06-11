from vpython import *

SCENE = canvas(width=800/1.3, height=600/1.3, align="left")
ROD_X = -scene.width + 50
SPRING_LEFT_X_OFFSET = 12
SPRING_LEFT_X = ROD_X + SPRING_LEFT_X_OFFSET
WHEEL_CENTER_X = 0
WHEEL_CENTER_Y = 0
NUM_SPRINGS = 1
GRAPH_HEIGHT = 300
GRAPH_WIDTH = 450
SPRING_STRETCHED_START_LENGTH = WHEEL_CENTER_X - (ROD_X + SPRING_LEFT_X_OFFSET)

def dist(p1, p2):
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

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

        #self.lever = helix(
        #         pos=vec(0,0,0),
        #         axis=self.lever_arm,
        #         color=color.cyan,
        #         radius=self.radius,
        #         length=(self.lever_arm_length),
        #         coils=self.length / self.radius,
        #)

    def change_config(self, evt, num=0, theta=0):
        changed_num = num if num == 0 else int(evt.id[-1])
        if "spr_const" in evt.id and changed_num == num:
            self.spr_const = evt.value
        if "spr_nat_len" in evt.id and changed_num == num:
            self.length = evt.value
        elif "spr_wheel_dist_y" in evt.id and changed_num == num:
            self.change_vertical_spr_wheel_dist(evt.value)
        elif "spr_wheel_dist_x" in evt.id and changed_num == num:
            self.change_horizontal_spr_wheel_dist(evt.value)
        elif "d_theta" in evt.id:
            self.update_position(theta)
        elif evt.id == "small_angle":
            self.small_angle = evt.checked

    def change_vertical_spr_wheel_dist(self, value):
        self.spring.pos = vec(SPRING_LEFT_X, value, 0)
        prev_x = self.lever_arm.x
        self.lever_arm = vec(prev_x, value, 0)
        self.lever_arm_length = sqrt(pow(prev_x, 2) + pow(value, 2))
        self.left_y_level = value
        #self.lever.visible = False
        #self.lever = helix(
        #         pos=vec(0, 0, 0),
        #         axis=self.lever_arm,
        #         color=color.cyan,
        #         radius=self.radius,
        #         length=(self.lever_arm_length),
        #         coils=self.length / self.radius,
        #)

    def change_horizontal_spr_wheel_dist(self, value):
        prev_y = self.lever_arm.y 
        self.lever_arm = vec(value, prev_y, 0)
        self.lever_arm_length = sqrt(pow(value, 2) + pow(prev_y, 2))
        prev_spring_length = self.spring.length
        self.spring.length = SPRING_STRETCHED_START_LENGTH + value
        self.spring.coils = self.spring.length / self.radius
        #self.lever.visible = False
        #self.lever = helix(
        #         pos=vec(0, 0, 0),
        #         axis=self.lever_arm,
        #         color=color.cyan,
        #         radius=self.radius,
        #         length=(self.lever_arm_length),
        #         coils=self.length / self.radius,
        #)

    def update_position(self, theta):
        if self.small_angle:
            if self.spring.pos.y < 0:
                self.spring.length += -theta * self.lever_arm_length
                self.lever_arm = rotate(self.lever_arm, angle=-theta, axis=vector(0, 0, 1))
            else:
                self.spring.length += theta * self.lever_arm_length
                self.lever_arm = rotate(self.lever_arm, angle=-theta, axis=vector(0, 0, 1))
            
            # self.arrow.visible = False
            # if self.spring.length < self.length:
            #     self.arrow = arrow(pos = self.lever_arm, axis = norm((self.spr_const * self.lever_arm_length) * self.axis) * 100, shaftwidth = 10)
            # elif self.spring.length > self.length:
            #     self.arrow = arrow(pos = self.lever_arm, axis = norm(-1 * ((self.spr_const * self.lever_arm_length) * self.axis)) * 100, shaftwidth = 10)
        else:
            self.lever_arm = rotate(self.lever_arm, angle=-theta, axis=vector(0, 0, 1))
            self.axis = self.lever_arm - self.spring.pos
            self.spring.visible = False
            self.spring = helix(pos=vec(SPRING_LEFT_X, self.left_y_level, 0),axis=self.axis,color=color.cyan,radius=self.radius,length=(mag(self.axis)),coils=self.length / self.radius)
        #self.lever.visible = False
        #self.lever = helix(
        #         pos=vec(0, 0, 0),
        #         axis=self.lever_arm,
        #         color=color.cyan,
        #         radius=self.radius,
        #         length=(self.lever_arm_length),
        #         coils=self.length / self.radius,
        #)
 
    def get_angular_frequency_component(self):
        if self.spring.length < self.length:
            return cross((self.spr_const * self.lever_arm_length) * self.axis, self.lever_arm)
        elif self.spring.length > self.length:
            return cross(-1 * ((self.spr_const * self.lever_arm_length) * self.axis),self.lever_arm)
        else:
            return vec(0, 0, 0)

    def get_torque(self):
        return cross(-1 * ((self.spr_const * (self.spring.length - self.length)) * self.axis),self.lever_arm)

    # def update(self):
    # where actual simulation goes
    # pass

class Wheel:
    def __init__(self, radius, mass, springs, extrusion=None, points=[]):
        self.points = points
        self.extrusion = extrusion
        self.extrusion_mode = (extrusion is not None)
        self.moved_com = False
        self.springs = springs
        self.mass = mass
        self.time = 0.0

        self.wheel = cylinder(pos=vec(WHEEL_CENTER_X, WHEEL_CENTER_Y, 0),axis=vec(WHEEL_CENTER_X, WHEEL_CENTER_Y, -1),radius=radius,length=1,color=color.red,make_trail=True)

        spoke1 = curve(pos=[vec(0, 0, 0), vec(radius, 0, 0)],color=color.black,radius=5)

        spoke2 = curve(pos=[vec(0, 0, 0), vec(0, radius, 0)],color=color.black,radius=5)

        spoke3 = curve(pos=[vec(0, 0, 0), vec(-radius, 0, 0)],color=color.black,radius=5)

        spoke4 = curve(pos=[vec(0, 0, 0), vec(0, -radius, 0)],color=color.black,radius=5)
        
        self.com = sphere(pos=vec(0, 0, 0), radius=10, color=color.black)
        self.com.visible = False

        self.spokes = [spoke1, spoke2, spoke3, spoke4]

        # self.springPoints = points(pos=self.springs, color=vec(0, 1, 0))

        self.calculateMomentOfInertia()

    def add_extrusion(self, extrusion, points):
        self.extrusion = extrusion
        self.points = points
        self.extrusion_mode = True
        self.calculate_com()

        self.calculateMomentOfInertia()

    def move_com_to_axis(self):
        translated_points = []
        for point in self.points:
            translated_points.append([point[0] - self.com.pos.x, point[1] - self.com.pos.y])
        shape = shapes.points(pos=translated_points)
        extrude = extrusion(path=[vec(0, 0, 0), vec(0, 0, -1)], shape=shape, color=color.red)
        self.extrusion.visible = False
        self.extrusion = extrude
        self.points = translated_points
        self.calculate_com()
        self.moved_com = True
    
    def get_vertical_line_extremas(self, x):
        y_one = 0
        y_two = 0
        if self.extrusion_mode:
            for i in range(len(self.points) - 2):
                first_point = self.points[i]
                second_point = self.points[i + 1]
        
                if first_point[0] > x and second_point[0] < x:
                    slope = (first_point[1] - second_point[1]) / (first_point[0] - second_point[0])
                    delta_y = slope * (x  - first_point[0])
                    y_one = first_point[1] + delta_y
                elif first_point[0] < x and second_point[0] > x:
                    slope = (first_point[1] - second_point[1]) / (first_point[0] - second_point[0])
                    delta_y = slope * (x - second_point[0])
                    y_two = second_point[1] + delta_y
        else:
            # x^2 + y^2 = r^2 
            # y^2 = r^2 - x^2 
            y2 = pow(self.wheel.radius, 2) - pow(x, 2)
            if y2 > 0:
                y = sqrt(y2)
                y_one = y
                y_two = -y
        return [max(y_one, y_two), min(y_one, y_two)]

    def get_horizontal_line_extremas(self, y):
        x_one = 0
        x_two = 0
        if self.extrusion_mode:
            for i in range(len(self.points) - 2):
                first_point = self.points[i]
                second_point = self.points[i + 1]
        
                if first_point[1] > y and second_point[1] < y:
                    slope = (first_point[0] - second_point[0]) / (first_point[1] - second_point[1])
                    delta_x = slope * (y  - first_point[1])
                    x_one = first_point[0] + delta_x
                elif first_point[1] < y and second_point[1] > y:
                    slope = (first_point[0] - second_point[0]) / (first_point[1] - second_point[1])
                    delta_x = slope * (y - second_point[1])
                    x_two = second_point[0] + delta_x
        else:
            # x^2 + y^2 = r^2 
            # x^2 = r^2 - y^2 
            x2 = pow(self.wheel.radius, 2) - pow(y, 2)
            if x2 > 0:
                x = sqrt(x2)
                x_one = x
                x_two = -x
        return [max(x_one, x_two), min(x_one, x_two)]

    def calculate_area(self):
        # using shoelace formula
        left_sum = 0
        right_sum = 0

        for i in range(len(self.points)):
                j = 0 if i == len(self.points) - 1 else i + 1
                left_sum += self.points[i][0] * self.points[j][1]
                right_sum += self.points[j][0] * self.points[i][1]

        return (0.5 * abs(left_sum - right_sum), 0.5 * (left_sum - right_sum))
    
    def calculate_com(self):
        # for two dimensional shapes, centroid is the center of mass
        # use a new formula for centroid of 2D polygon w/ shoelace
        # can use this later in parallel axis theorem

        x_sum = 0
        y_sum = 0
        for i in range(len(self.points)):
            j = 0 if i == len(self.points) - 1 else i + 1
            x_sum += (self.points[i][0] + self.points[j][0]) * (self.points[i][0] * self.points[j][1] - self.points[j][0] * self.points[i][1])
            y_sum += (self.points[i][1] + self.points[j][1]) * (self.points[i][0] * self.points[j][1] - self.points[j][0] * self.points[i][1])
        
        area = self.calculate_area()[1] # signed area
        self.com.visible = False
        self.com = sphere(pos=vec(x_sum / (6 * area), y_sum / (6 * area), 0), radius=10, color=color.black) 
        return vec(x_sum / (6 * area), y_sum / (6 * area), 0)
    
    def calculate_area_inertia_x(self):
        # use collarary to shoelace formula for moment of inertia of 2D polygon
        sum = 0
        for i in range(len(self.points)):
            j = 0 if i == len(self.points) - 1 else i + 1
            sum += (self.points[i][0] * self.points[j][1] - self.points[j][0] * self.points[i][1]) * (self.points[i][1] ** 2 + self.points[i][1] * self.points[j][1] + self.points[j][1] ** 2)

        return abs(sum / 12)

    def calculate_area_inertia_y(self):
        sum = 0
        for i in range(len(self.points)):
            j = 0 if i == len(self.points) - 1 else i + 1
            sum += (self.points[i][0] * self.points[j][1] - self.points[j][0] * self.points[i][1]) * (self.points[i][0] ** 2 + self.points[i][0] * self.points[j][0] + self.points[j][0] ** 2)

        return abs(sum / 12)

    def calculateMomentOfInertia(self):
        if self.extrusion is not None:
            # calculate area moment of inertia for the shape about the x-axis
            # calculate area moment of inertia for the shape about the y-axis
            # find the area moment of inertia about of the z-axis (sum, polar moment of inertia)
            # use parallel-axis theorem and com (centroid) to find the moment of inertia about the center of mass => extrapolate for other points maybe

            Ix = self.calculate_area_inertia_x()
            Iy = self.calculate_area_inertia_y()
            J = Ix + Iy # polar moment of inertia about origin

            area = self.calculate_area()[0]
            com = self.calculate_com()

            dist_to_com = dist((0, 0), (com.x, com.y))
            J_com = J - area * dist_to_com ** 2
            
            self.momentOfInertia = (self.mass / area) * J_com
            
        else:
            self.momentOfInertia = 0.5 * self.mass * pow(self.wheel.radius, 2)
            

    def change_config(self, evt, theta=0):
        if evt.id == "mass":
            self.mass = evt.value
            self.calculateMomentOfInertia()

        elif evt.id == "radius" and not self.extrusion:
            self.wheel.radius = evt.value
            self.spokes[0].modify(1, pos=vec(evt.value, 0, 0))
            self.spokes[1].modify(1, pos=vec(0, evt.value, 0))
            self.spokes[2].modify(1, pos=vec(-evt.value, 0, 0))
            self.spokes[3].modify(1, pos=vec(0, -evt.value, 0))
            self.calculateMomentOfInertia()

        elif evt.id == "d_theta":
            self.update_position(theta)

    def update_position(self, theta):
        if self.extrusion_mode:
            self.extrusion.rotate(axis=vec(0,0,1), angle = -theta, origin = vec(0,0,0))
            if not self.moved_com:
                self.com.rotate(axis=vec(0,0,1), angle = -theta, origin = vec(0,0,0))
        else:
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

    def calculate_angular_accel(self):

        total_torque = 0

        for spring in self.springs:
            total_torque += spring.get_torque().z

        if not self.moved_com:
            com_lever_arm = self.com.pos
            fg = vec(0,-9.81 * self.mass, 0)
            tg = cross(com_lever_arm, fg)
            total_torque += tg.z
        return total_torque / self.momentOfInertia

    # def update(self):
    # where the actual simulation goes
    # self.springPoints = points(pos=self.springLocations, color=vec(0, 1, 0))
    # pass

class Simulation:
    def __init__(self):
        self.run = False
        self.pause = False
        self.small_angle_mode = True
        self.preset_mode = False
        self.angular_displace_mode = False
        self.previous_theta = 0
        self.small_angle = True
        self.small_angle_disabled = False
        self.draw = False
        self.custom_object = False
        self.moved_com = False
        self.pole = Pole()
        self.spring_arr = [Spring(length=(SPRING_STRETCHED_START_LENGTH),radius=30,spr_wheel_dist=120,spr_const=2)]
        self.custom_points = []

        self.num_springs = 1
        self.wheel = Wheel(radius=200, mass=15, springs=self.spring_arr)

        self.ang_pos_graph = graph(width=GRAPH_WIDTH, height=GRAPH_HEIGHT,title="Angular Position vs Time",xtitle="Time (s)",ytitle="Angular Position (rad)", align="left")
        self.ang_pos_curve = gcurve(color=color.blue)
        self.ang_vel_graph = graph(width=GRAPH_WIDTH,height=GRAPH_HEIGHT,title="Angular Velocity vs Time",xtitle="Time (s)",ytitle="Angular Velocity (rad/s)", align="left")
        self.ang_vel_curve = gcurve(color=color.green)
        self.ang_acc_graph = graph(width=GRAPH_WIDTH,height=GRAPH_HEIGHT,title="Angular Acceleration vs Time",xtitle="Time (s)",ytitle="Angular Acceleration (rad/s^2)", align="left")
        self.ang_acc_curve = gcurve(color=color.orange)

        self.inputs = []
        self.spr_wheel_dist_texts = []
        self.spr_wheel_dist_x_texts = []
        self.spr_const_texts = []
        self.spr_nat_len_texts = []

        sphere(pos = vec(0,0,0), radius = 15, color = color.white * 0.5)
        sphere(pos = vec(500,-400, 0), radius = 15, color = color.white * 0.5)
        text(pos = vec(520, -410, 0), text = " - Axis of rotation", height = 30, color = color.black)

    def loop(self):
        for i in range(len(self.inputs)):
            if i >= 3:  # first three is the run, reset, pause simulation buttons
                self.inputs[i].delete()

        if self.small_angle:
            theta_amplitude = abs(self.previous_theta)
            time_step = 0
            while self.run:
                while self.pause:
                    sleep(0.5)
                angular_pos = theta_amplitude * cos(self.angular_frequency * time_step)
                angular_velocity = (-theta_amplitude* self.angular_frequency* sin(self.angular_frequency * time_step))
                angular_acceleration = (-theta_amplitude* pow(self.angular_frequency, 2)* cos(self.angular_frequency * time_step))
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
            self.custom_points.append(sphere(pos=SCENE.mouse.pos, radius=12.5, color=color.black))

    def setup(self):
        SCENE.background = color.white

        SCENE.center = vec(0, 0, 0)
        SCENE.forward = vec(0, 0, -1)
        SCENE.up = vec(0, 1, 0)
        SCENE.range = 660

        SCENE.userzoom = False
        SCENE.userspin = False
        SCENE.userpan = False

        while not self.run:
            if self.draw:
                SCENE.bind('click', self.add_custom_point)
            
            # for input in self.inputs:
            # input.visible = False
            self.inputs = []
            #for spring in self.spring_arr:
                #pass

            SCENE.caption = ""
            self.instructions()
            self.menu()
            for spring in self.spring_arr:
                    extremas = self.wheel.get_vertical_line_extremas(SPRING_LEFT_X+ spring.spring.length)
                    
                    max_val = extremas[0]
                    min_val = extremas[1]
                    if max_val == 0 and min_val == 0:
                        spring.change_horizontal_spr_wheel_dist(0)
                        extremas = self.wheel.get_vertical_line_extremas(0)
                    if spring.spring.pos.y > max_val:
                        spring.change_vertical_spr_wheel_dist(max_val)
                    elif spring.spring.pos.y < min_val:
                        spring.change_vertical_spr_wheel_dist(min_val)
            sleep(0.5)

        self.angular_frequency = self.wheel.calculate_angular_frequency()

    def instructions(self):
        SCENE.append_to_caption(
            "     <b>Spring-Wheel Oscillation Simulation</b>\n"
            "     -----------------------------------------------------------------\n"
            "     Use the controls below to set up and run the simulation.\n\n"

            "     1. Choose whether to use the small angle approximation. (Some features are <b>not</b> available in small angle mode)\n"
            "     2. Click Set Small Angle Mode button.\n"
            "     3. Adjust the wheel, spring, and mass settings with the sliders. Then, press the Set Presets button.\n"
            "     4. Set the starting angular displacement.\n"
            "     5. Click Run Simulation to begin.\n\n"

            "     <b>Another Important Feature</b>: Draw Custom Object lets you create your own rotating shape.\n"
            "     After pressing the button, proceed to plot points on the screen.\n\n"
            "     <b>NOTE:</b> Points must be plotted in a <u>clockwise</u> or <u>counterclockwise</u> manner to create a\n"
            "     closed shape. After plotting at least 3 points, click Finish Custom Object to create the shape\n"
            "     and attach it to the wheel. You can then choose to either move the center of mass to the axis of\n"
            "     rotation or leave it in its original position. <b>Important! If the object you drew is not attached to the \n" 
            "     axis of rotation, you MUST press the button to move the center of mass to the axis.</b> All springs are \n" 
            "     initially at natural length.\n\n"
            "     <b>NOTE:</b> Please refrain from holding down your mouse while using the input menu since it's\n"
            "     <u>constantly updating every 0.5 seconds</u> in a loop. Instead, please click! This ensures a good user \n"
            "     experience and prevents any potential issues with the inputs. Also <u>allow about a second for your</u> \n"
            "     <u>inputs to register.</u>\n\n"
            "     Use Pause/Unpause to stop or continue the motion, and Reset Simulation to start over.\n\n\n"
        )

    def menu(self):
        ### RUN SIM BUTTON ### IMPORTANT: MUST BE FIRST OR SECOND IN INPUTS LIST!!!!!
        SCENE.append_to_caption("     ")
        if self.small_angle_mode:
            def bind_set_small_angle(_):
                self.small_angle_mode = False
                self.preset_mode = True
                self.small_angle_disabled = True
                
            self.inputs.append(button(bind=bind_set_small_angle, text="Set Small Angle Mode"))

        elif self.angular_displace_mode or self.run:
            def bind_run(_):
                self.run = True
                self.angular_displace_mode = False

            self.inputs.append(button(bind=bind_run, text="Run Simulation"))
        elif self.preset_mode:
            def bind_preset(_):
               self.preset_mode = False
               self.angular_displace_mode = True
 
            self.inputs.append(button(bind=bind_preset, text="Set Presets"))

        SCENE.append_to_caption("   ")

        ### RESET SIM BUTTON ### IMPORTANT: MUST BE FIRST OR SECOND IN INPUTS LIST!!!!!
        def bind_reset(_):
            for item in SCENE.objects:
                item.visible = False
                del item

            self.run = False
            self.pause = False
            self.angular_displace_mode = False
            self.preset_mode = False
            self.small_angle_mode = True
            self.custom_points = []
            self.custom_object = False
            self.draw = False
            self.previous_theta = 0
            self.small_angle = True
            self.small_angle_disabled = False
            self.draw = False
            self.moved_com = False
            self.pole = Pole()
            self.spring_arr = [Spring(length=(SPRING_STRETCHED_START_LENGTH),radius=30,spr_wheel_dist=120,spr_const=2)]  # use single spring for now

            self.ang_pos_graph.delete()
            self.ang_vel_graph.delete()
            self.ang_acc_graph.delete()
            self.wheel = Wheel(radius=200, mass=15, springs=self.spring_arr)

            self.ang_pos_graph = graph(width=GRAPH_WIDTH, height=GRAPH_HEIGHT,title="Angular Position vs Time",xtitle="Time (s)",ytitle="Angular Position (rad)", align="left")
            self.ang_pos_curve = gcurve(color=color.blue)
            self.ang_vel_graph = graph(width=GRAPH_WIDTH,height=GRAPH_HEIGHT,title="Angular Velocity vs Time",xtitle="Time (s)",ytitle="Angular Velocity (rad/s)", align="left")
            self.ang_vel_curve = gcurve(color=color.green)
            self.ang_acc_graph = graph(width=GRAPH_WIDTH,height=GRAPH_HEIGHT,title="Angular Acceleration vs Time",xtitle="Time (s)",ytitle="Angular Acceleration (rad/s^2)", align="left")
            self.ang_acc_curve = gcurve(color=color.orange)

            sphere(pos = vec(0,0,0), radius = 15, color = color.white * 0.5)
            sphere(pos = vec(500,-400, 0), radius = 15, color = color.white * 0.5)
            text(pos = vec(520, -410, 0), text = " - Axis of rotation", height = 30, color = color.black)

        self.inputs.append(button(bind=bind_reset, text="Reset Simulation"))
        SCENE.append_to_caption("   ")

        ## PAUSE SIM BUTTON ###
        def bind_pause(_):
            self.pause = not self.pause

        self.inputs.append(button(bind=bind_pause, text="Pause/Unpause Simulation"))
        
        SCENE.append_to_caption("\n\n")

        ## DRAW OBJECT BUTTON ###
        if self.preset_mode and not (self.draw or self.custom_object):
            def bind_draw(_):
                self.draw = True

            SCENE.append_to_caption("     ")
            self.inputs.append(button(bind=bind_draw, text="Draw Custom Object")) 
            SCENE.append_to_caption("  \n")

        ### DRAW FINISH BUTTON ###
        def bind_draw_finish(_):
            if len(self.custom_points) < 3:
                pass # do nothing if you can't create closed object
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
                self.wheel.add_extrusion(extrude, two_d_points)
                self.draw = False
                self.small_angle = False
                self.small_angle_disabled = True
                for spring in self.spring_arr:
                    spring.small_angle = False
                sphere(pos = vec(500,-450, 0), radius = 10, color = color.black)
                text(pos = vec(520, -460, 0), text = " - Center of Mass", height = 30, color = color.black)

                #self.wheel.move_com_to_axis()
        
        if self.draw:
            SCENE.append_to_caption("     ")
            self.inputs.append(button(bind=bind_draw_finish, text="Finish Custom Object"))

        if not self.custom_object:
            SCENE.append_to_caption("   ")

        ### MOVE C.O.M ###
        if self.preset_mode and self.custom_object and not self.draw and not self.moved_com:
            def bind_move_com():
                self.wheel.move_com_to_axis()
                self.moved_com = True 
            SCENE.append_to_caption("     ")
            self.inputs.append(button(bind= bind_move_com, text = "Move C.O.M To Axis of Rotation/Attach Object to Axis of Rotation"))
            SCENE.append_to_caption("\n\n")

        ### DRAW UNDO BUTTON ###
        def bind_draw_undo(_):
            if len(self.custom_points) > 0:
                self.custom_points[-1].visible = False
                self.custom_points[-1].delete()
                self.custom_points.pop()
        
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
            SCENE.append_to_caption("  \n")
 
        if not self.custom_object:
            SCENE.append_to_caption("\n")
       # SMALL ANGLE APPROX CHECKBOX
        def angle_aprox_bind(evt):
            self.small_angle = evt.checked
            for spring in self.spring_arr:
                spring.change_config(evt=evt)
        
        if self.small_angle_mode or self.preset_mode:
            SCENE.append_to_caption("     ")
            SCENE.append_to_caption("Small Angle Approximation?: ")
            self.small_angle_checkbox = checkbox(bind=angle_aprox_bind, checked=self.small_angle, id="small_angle")
            self.small_angle_checkbox.disabled = self.small_angle_disabled
            if self.small_angle_disabled and self.custom_object:
                SCENE.append_to_caption(" (Small Angle Approx set to false for custom object)")
            self.inputs.append(self.small_angle_checkbox);

            SCENE.append_to_caption("\n\n") 

        ### ANGULAR DISPLACEMENT SLIDER ###
        
        def d_theta_bind(evt):
            d_theta_text.text = str(evt.value) + " rad\n"
            
            new_value = evt.value - self.previous_theta
            self.previous_theta = evt.value
            
            for spring in self.spring_arr:
                spring.change_config(evt=evt, theta=new_value)

            self.wheel.change_config(evt=evt, theta=new_value)

        if self.angular_displace_mode:
            SCENE.append_to_caption("     ")
            SCENE.append_to_caption("Angular Displacement: ")
            self.inputs.append(slider(bind=d_theta_bind,min=radians(-30) if self.small_angle else radians(-180),value=self.previous_theta,max=radians(30) if self.small_angle else radians(180),step=radians(5),length=200,id="d_theta"))
            d_theta_text = wtext(text=str(self.previous_theta) + " rad\n")
            SCENE.append_to_caption("\n\n\n\n")

        ### MASS SLIDER ###
        def mass_bind(evt):
            mass_text.text = str(evt.value) + " kg\n"
            self.wheel.change_config(evt=evt)  # cleanup in future

        if self.preset_mode:
            SCENE.append_to_caption("     ")
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
            
            if self.preset_mode:
                SCENE.append_to_caption("     ")
                SCENE.append_to_caption("Wheel Radius: ")
                self.inputs.append(slider(bind=radius_bind,min=50,value=self.wheel.wheel.radius,max=300,step=1,length=200,id="radius"))
                radius_text = wtext(text=str(self.wheel.wheel.radius) + " m\n")

        ### NUMBER OF SPRINGS DROPDOWN ###
        def num_springs_bind(evt):
            if evt.value > len(self.spring_arr):
                self.spring_arr.append(Spring(length=(SPRING_STRETCHED_START_LENGTH),radius=30,spr_wheel_dist=evt.value,spr_const=2,small_angle = self.small_angle))
            elif evt.value < len(self.spring_arr):
                self.spring_arr[-1].spring.visible = False
                self.spring_arr[-1].spring.delete()
                self.spring_arr.pop()

            num_springs_text.text = str(evt.value) + " springs \n"

        if self.preset_mode:
            SCENE.append_to_caption("     ")
            SCENE.append_to_caption("Number of Springs: ")
            self.inputs.append(slider(bind=num_springs_bind,min=1,max=3,value=len(self.spring_arr),step=1,length=200))
            num_springs_text = wtext(text=str(len(self.spring_arr)) + " springs \n")
            SCENE.append_to_caption("\n")

        ### SPRING CONSTANT SLIDER ###
        def spr_const_bind(evt):
            self.spr_const_texts[int(evt.id[-1])].text = str(evt.value) + " N/m\n"
            for i in range(len(self.spring_arr)):
                self.spring_arr[i].change_config(evt=evt, num=i + 1)

        if self.preset_mode:
            for i in range(len(self.spring_arr)):
                SCENE.append_to_caption("     ")
                SCENE.append_to_caption(f"Spring {i + 1} Constant: ")
                self.inputs.append(slider(bind=spr_const_bind,min=0.5,max=5,value=self.spring_arr[i].spr_const,step=0.1,length=200,id=f"spr_const_{i + 1}"))
                self.spr_const_texts.append(wtext(text=str(self.spring_arr[i].spr_const) + " N/m\n"))

        ### SPRING NATURAL LENGTH ### 
        def spr_nat_len_bind(evt):
            self.spr_nat_len_texts[int(evt.id[-1])].text = str(evt.value) + " m\n"
            for i in range(len(self.spring_arr)):
                self.spring_arr[i].change_config(evt=evt, num = i + 1)

        if self.preset_mode and not self.small_angle: 
            for i in range(len(self.spring_arr)):
                SCENE.append_to_caption("     ")
                SCENE.append_to_caption(f"Spring {i + 1} Natural Length: ")
                self.inputs.append(slider(bind=spr_nat_len_bind, min = 0.5 * SPRING_STRETCHED_START_LENGTH, max = 1.5 * SPRING_STRETCHED_START_LENGTH, value = self.spring_arr[i].length, step = 0.1, length = 200, id = f"spr_nat_len_{i+1}"))
                self.spr_nat_len_texts.append(wtext(text=str(self.spring_arr[i].length) + " m\n"))

        ### SPRING-WHEEL DISTANCE Y SLIDER ###
        def spr_wheel_dist_bind_y(evt):
            self.spr_wheel_dist_texts[int(evt.id[-1]) - 1].text = (str(evt.value) + " m\n")
            for i in range(len(self.spring_arr)):
                self.spring_arr[i].change_config(evt=evt, num=i + 1)

        if self.preset_mode:
            for i in range(len(self.spring_arr)):
                SCENE.append_to_caption("     ")
                SCENE.append_to_caption(f"Spring {i + 1}-Wheel Distance Y:")
                extremas = self.wheel.get_vertical_line_extremas(SPRING_LEFT_X + self.spring_arr[i].spring.length)
                min_val = extremas[1]
                max_val = extremas[0]
                self.inputs.append(slider(bind=spr_wheel_dist_bind_y,min=min_val,max=max_val,value=self.spring_arr[i].spring.pos.y,step=1,length=200,id=f"spr_wheel_dist_y_{i + 1}"))
                self.spr_wheel_dist_texts.append(wtext(text=str(self.spring_arr[i].spring.pos.y) + " m\n"))

        ### SPRING-WHEEL DISTANCE X SLIDER ###
        def spr_wheel_dist_bind_x(evt):
            self.spr_wheel_dist_x_texts[int(evt.id[-1]) - 1].text = (str(evt.value) + " m\n")

            for i in range(len(self.spring_arr)):
                self.spring_arr[i].change_config(evt=evt, num=i + 1)

        if self.preset_mode and not self.small_angle:
            for i in range(len(self.spring_arr)):
                SCENE.append_to_caption("     ")
                SCENE.append_to_caption(f"Spring {i + 1}-Wheel Distance X:")
                extremas = self.wheel.get_horizontal_line_extremas(self.spring_arr[i].left_y_level)
                min_val = extremas[1]
                max_val = extremas[0]
                self.inputs.append(slider(bind=spr_wheel_dist_bind_x, min=min_val, max=max_val, value=SPRING_LEFT_X + self.spring_arr[i].spring.length, id=f"spr_wheel_dist_x_{i + 1}", step=1, length=200))
                self.spr_wheel_dist_x_texts.append(wtext(text=str(SPRING_LEFT_X + self.spring_arr[i].spring.length) + " m\n"))

if __name__ == "__main__":
    simulation = Simulation()
    while True:
        simulation.setup()

        run = False
        while not run:
            run = simulation.run

        if run:
            simulation.loop()
