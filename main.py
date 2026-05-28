from simulation import Simulation

if __name__ == "__main__":
    simulation = Simulation()
    simulation.setup()

    while True: 
        run = False
        while not run:
            run = simulation.run
    
        simulation.loop()

        while run: 
            run = simulation.run

        
        simulation = Simulation()
        simulation.setup()
    