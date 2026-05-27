from simulation import Simulation

if __name__ == "__main__":
    simulation = Simulation()
    simulation.setup()

    while 1:
        simulation.loop()
