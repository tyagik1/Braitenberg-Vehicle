import agent
import numpy as np

class History():
    def __init__(self, xHistory, yHistory):
        # Stores the recorded x and y positions over time
        self.xHistory = xHistory
        self.yHistory = yHistory

def simPopulation(focus, population, duration):
    # Simulates a population of identical bots (same agent object),
    # each run independently for the same duration.
    histories = []
    displacements = []
    explorations = []

    for i in range(population):
        # Run one bot simulation
        history, displacement, exploration = simBot(focus, duration)
        histories.append(history)
        displacements.append(displacement)
        explorations.append(exploration)
    
    # Returns movement histories, displacement arrays, and exploration amounts
    return histories, displacements, explorations

def simBot(focus, duration):
    # Tracks x,y positions over time for a single bot
    xHistory = np.zeros(duration + 1)
    yHistory = np.zeros(duration + 1)

    # Initial position
    xHistory[0] = focus.x
    yHistory[0] = focus.y
    
    # 2D grid storing visited locations
    pathing = []

    # The grid dimensions are sqrt(duration) × sqrt(duration)
    size = int(np.sqrt(duration))

    # Initialize a 2D grid of zeros
    for i in range(size):
        path = []
        for j in range(size):
            path.append(0)
        pathing.append(path)

    # Start pathing from the grid center
    posX = size // 2
    posY = size // 2

    # Mark starting cell as visited
    pathing[posX][posY] = 1

    # Simulate movement for the given duration
    for i in range(duration):
        focus.turn()  # Agent determines new heading
        focus.step()  # Agent moves forward based on velocity
        xHistory[i+1] = focus.x
        yHistory[i+1] = focus.y

        # Compute integer travel distances in x and y directions
        xTravel = abs(int(focus.v * np.cos(focus.o)))
        yTravel = abs(int(focus.v * np.sin(focus.o)))

        # Mark every grid cell passed through as visited
        for j in range(xTravel):
            for k in range(yTravel):
                # Ensure indexing stays in bounds to avoid crashes
                if 0 <= j + posX < size and 0 <= k + posY < size:
                    pathing[j + posX][k + posY] = 1
        
        # Update current grid position
        posX += xTravel
        posY += yTravel
    
    # Count how many grid cells were visited
    exploration = 0
    
    for i in range(size):
        for j in range(size):
            if pathing[i][j] == 1:
                exploration += 1
    
    # Store path history
    history = History(xHistory, yHistory)

    # Displacement array: distance from origin at every time step
    displacement = np.sqrt(xHistory**2 + yHistory**2)

    return history, displacement, exploration

def runRandom(population, duration, numTypes):
    # Creates each of the random walker types and simulates them
    agents = []

    # Instantiate the three different random walker types
    firstBorn = agent.RandomWalker()
    secondBorn = agent.TrulyRandomWalker(duration)
    thirdBorn = agent.RandomRandomWalker(duration)

    agents.append(firstBorn)
    agents.append(secondBorn)
    agents.append(thirdBorn)

    # Run population simulations for the selected number of agent types
    for i in range(numTypes):
        histories, displacements, explorations = simPopulation(agents[i], population, duration)

        # Save results for later analysis
        np.save(f"histories{i}.npy", histories)
        np.save(f"displacements{i}.npy", displacements)
        np.save(f"explorations{i}.npy", explorations)

def simVehicle(vehicle, duration, light):
    # Simulates a single Braitenberg vehicle moving toward a light source
    xHistory = np.zeros(duration + 1)
    yHistory = np.zeros(duration + 1)

    # Starting position
    xHistory[0] = vehicle.x
    yHistory[0] = vehicle.y

    # Simulation loop
    for i in range(duration):
        vehicle.sense(light, int(np.sqrt(duration)))     # Detects light intensity
        vehicle.think(duration)  # Can use thinkWorldWide() instead for 10,000 steps for World-Wide movement
        vehicle.move()           # Applies movement based on sensor → motor mapping
        xHistory[i+1] = vehicle.x
        yHistory[i+1] = vehicle.y
    
    # Return the recorded trajectory
    history = History(xHistory, yHistory)

    return history

def runVehicle(duration, numLights):
    # Runs a Braitenberg simulation for multiple random light source placements
    for i in range(numLights):
        light = agent.LightSource(int(np.sqrt(duration)))  # Random light location
        vehicle = agent.Braitenberg()                      # New vehicle instance

        # Simulate vehicle behavior
        history = simVehicle(vehicle, duration, light)

        # Store the light’s coordinates
        lightXY = np.zeros(2)
        lightXY[0] = light.x
        lightXY[1] = light.y

        # Save results
        np.save(f"history{i}.npy", history)
        np.save(f"lightXY{i}.npy", lightXY)

def part1(population, duration, numTypes):
    # Make sure to use part 1 turning for the random vehicles
    runRandom(population, duration, numTypes)

def part2(population, duration, numTypes):
    # Make sure to use part 2 turning for the random vehicles
    runRandom(population, duration, numTypes)

def part3(duration, numLights):
    # Can use thinkWorldWide() instead for 10,000 steps for World-Wide movement
    runVehicle(duration, numLights)

population = 5 # Number of bots

duration = 10000 # Number of steps

numTypes = 3 # Change to 1 for part 1 and 3 for part 2

numLights = 10

# Uncomment the part that you want to run

# part1(population, duration, numTypes) # Make sure to use part 1 turning for the random vehicles

# part2(population, duration, numTypes) # Make sure to use part 2 turning for the random vehicles

part3(duration, numLights) # Can use thinkWorldWide() instead for 10,000 steps for World-Wide movement