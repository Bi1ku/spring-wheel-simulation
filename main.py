from simulation import Simulation

if __name__ == "__main__":
    simulation = Simulation()
    simulation.setup()

    run = False
    while not run:
        run = simulation.run
    
    if run:
        simulation.loop()
