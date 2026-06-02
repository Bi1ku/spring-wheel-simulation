class CustomObject:
    def __init__(self, name, value, extrusion, mass, springs):
        self.springs = springs
        self.name = name
        self.mass = mass
        self.value = value

        self.extrusion = extrusion

    def calculate_moment_of_inertia(self):
        pass

    def change_config(self, evt):
        pass

    def update_position(self, theta):
        pass
