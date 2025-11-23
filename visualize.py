import matplotlib.pyplot as plt
import numpy as np
import sim


# -----------------------------
# Helper Functions
# -----------------------------

def findExploredRandom(histories, explorations):
    results = []

    for t in range(sim.numTypes):
        type_values = []
        for r in range(sim.population):
            x = histories[t][r].xHistory
            y = histories[t][r].yHistory

            x_range = max(x) - min(x)
            y_range = max(y) - min(y)

            size = (x_range * (y_range + 1)) + (y_range * (x_range + 1))

            type_values.append(explorations[t][r] / size)

        results.append(type_values)

    return results


# -----------------------------
# Visualization Functions
# -----------------------------

def showPathRandom(histories, displacements):
    for t in range(sim.numTypes):
        for r in range(sim.population):
            x = histories[t][r].xHistory
            y = histories[t][r].yHistory

            plt.plot(x, y)
            plt.plot(x[0], y[0], 'ro')   # Start
            plt.plot(x[-1], y[-1], 'ko') # End

            plt.xlabel("x")
            plt.ylabel("y")
            plt.title(f"Type {t + 1} Robot {r + 1} Movement")
            plt.show()


def showAverageDisplacementRandom(displacements):
    for t in range(sim.numTypes):
        avg_vals = []

        for time in range(sim.duration + 1):
            total = sum(displacements[t][r][time] for r in range(sim.population))
            avg_vals.append(total / sim.population)

        plt.plot(avg_vals)
        plt.xlabel("Time")
        plt.ylabel("Average Displacement")
        plt.title(f"Type {t + 1} Robot Average Displacement")
        plt.show()


def showHistogramRandom(explores):
    colors = ["blue", "orange", "green", "red", "purple", "gray"]

    all_data = np.concatenate(explores)
    bins = np.histogram_bin_edges(all_data, bins=50)

    for t in range(sim.numTypes):
        plt.hist(
            explores[t],
            bins=bins,
            alpha=0.5,
            color=colors[t],
            edgecolor=colors[t],
            label=f"Type {t + 1}"
        )

    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.title("Exploration Histogram")
    plt.legend(title="Robot Types")
    plt.show()


def printStatsRandom(explores):
    for t in range(sim.numTypes):
        values = explores[t]
        print(f"For type {t + 1}:")
        print(f"  Mean: {np.mean(values)}")
        print(f"  Median: {np.median(values)}")
        print(f"  Max: {np.max(values)}")
        print(f"  Min: {np.min(values)}")
        print(f"  Std Dev: {np.std(values)}\n")


# -----------------------------
# Reading Data
# -----------------------------

def readRandom():
    histories = []
    displacements = []
    explorations = []

    for t in range(sim.numTypes):
        histories.append(np.load(f"histories{t}.npy", allow_pickle=True))
        displacements.append(np.load(f"displacements{t}.npy", allow_pickle=True))
        explorations.append(np.load(f"explorations{t}.npy", allow_pickle=True))

    return histories, displacements, explorations


def readVehicle():
    history = []
    lightXY = []

    for i in range(sim.numLights):
        history.append(np.load(f"history{i}.npy", allow_pickle=True).item())
        lightXY.append(np.load(f"lightXY{i}.npy", allow_pickle=True))

    return history, lightXY


# -----------------------------
# Braitenberg Vehicle Scoring / Visualization
# -----------------------------

def getFitnessScore(history, lightXY, idx):
    hx = history[idx].xHistory
    hy = history[idx].yHistory

    lx, ly = lightXY[idx]

    start_dist = np.sqrt((hx[0] - lx)**2 + (hy[0] - ly)**2)
    end_dist = np.sqrt((hx[-1] - lx)**2 + (hy[-1] - ly)**2)

    score = np.clip(1 - (end_dist / start_dist), 0, 1)
    return score


def getTotalFitnessScore(history, lightXY):
    total = 0

    for i in range(sim.numLights):
        total += getFitnessScore(history, lightXY, i)

    return total / sim.numLights


def showPathVehicle(history, lightXY):
    for i in range(sim.numLights):
        x = history[i].xHistory
        y = history[i].yHistory
        lx, ly = lightXY[i]

        plt.plot(lx, ly, 'mo')  # Light source
        plt.plot(x, y)
        plt.plot(x[0], y[0], 'ro')
        plt.plot(x[-1], y[-1], 'ko')

        plt.xlabel("x")
        plt.ylabel("y")
        plt.title(f"Vehicle {i + 1} Path")
        plt.show()

        print(
            f"Vehicle {i + 1}:\n"
            f"  Start: ({x[0]}, {y[0]})\n"
            f"  End: ({x[-1]}, {y[-1]})\n"
            f"  Light: ({lx}, {ly})\n"
            f"  Score: {getFitnessScore(history, lightXY, i)}\n"
        )


def showVehicleTogether(history, lightXY):
    for i in range(sim.numLights):
        x = history[i].xHistory
        y = history[i].yHistory
        lx, ly = lightXY[i]

        plt.plot(lx, ly, 'mo')
        plt.plot(x, y)

        plt.plot(x[0], y[0], 'ro')
        plt.plot(x[-1], y[-1], 'ko')

        print(
            f"Vehicle {i + 1}:\n"
            f"  Start: ({x[0]}, {y[0]})\n"
            f"  End: ({x[-1]}, {y[-1]})\n"
            f"  Light: ({lx}, {ly})\n"
            f"  Score: {getFitnessScore(history, lightXY, i)}\n"
        )

    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("All Vehicles Path Overview")
    plt.show()

    print(f"Overall Fitness Score = {getTotalFitnessScore(history, lightXY)}")

# -----------------------------
# Run Sections
# -----------------------------

def part1Visualize():
    histories, displacements, explorations = readRandom()
    showPathRandom(histories, displacements)
    showAverageDisplacementRandom(displacements)


def part2Visualize():
    histories, displacements, explorations = readRandom()
    showPathRandom(histories, displacements)

    explores = findExploredRandom(histories, explorations)
    showHistogramRandom(explores)
    printStatsRandom(explores)


def part3Visualize():
    history, lightXY = readVehicle()
    showPathVehicle(history, lightXY)
    showVehicleTogether(history, lightXY)


# Choose what to run
# part1Visualize()
# part2Visualize()
part3Visualize()