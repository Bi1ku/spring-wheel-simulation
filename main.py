from simulation import Simulation

if __name__ == "__main__":
    simulation = Simulation(0.5, 0.1)
    simulation.setup()
    simulation.loop()
