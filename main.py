from simulation import Simulation

if __name__ == "__main__":
    simulation = Simulation()
    simulation.setup()

    simulation.loop()

    #while True:
    #    if simulation.run:
    #        simulation.loop()
