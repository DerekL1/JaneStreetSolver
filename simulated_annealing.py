# using simulated annealing, an improvement on hill climbing that utilizes cooling rates to maximize explorations vs exploitation in order to find a global optimum
# imports
from solver import outside_score
import random
import numpy as np
from hill_climbing import hill_climb

# globals
global ALPHABET, final_puzzle, final_score
ALPHABET = "ABCDEFGHIJKLMNOPRSTUVWXYZ"
final_puzzle = ""
final_score = 0

# simulated annealing parameters
INITIAL_TEMPERATURE = 100.0
MIN_TEMPERATURE = 0.01
COOLING_RATE = 0.99
ITERATIONS_PER_TEMPERATURE = 500

# function to calculate acceptance probability
def acceptance_probability(current_energy, new_energy, temperature):
    # if new puzzle is better than old puzzle, guarantee acceptance
    if new_energy > current_energy:
        return 1.0
    # if not find the exponential of the difference
    else:
        delta_energy = new_energy - current_energy
        scaled_delta = delta_energy / 1000000 # scale the delta to match the point range
        return np.exp(scaled_delta / np.sqrt(temperature))
    
# function to generate a random initial puzzle
def generate_initial_puzzle():
    return "".join([random.choice(ALPHABET) for i in range(25)])

def simulated_annealing(current_puzzle):
    global final_puzzle, final_score
    # create starting values
    current_energy = outside_score(current_puzzle)[0]
    temperature = INITIAL_TEMPERATURE
    max_puzzle, max_score = "", 0
    # loop until temperature has cooled to a fixed minimum
    while temperature > MIN_TEMPERATURE:
        for _ in range(ITERATIONS_PER_TEMPERATURE):
            # generate a neighboring puzzle by randomly changing one index's letter
            i = random.randint(0, 24)
            letter = random.choice(ALPHABET)
            new_puzzle = current_puzzle[:i] + letter + current_puzzle[i+1:]
            # calculate the new puzzle's points and update maxes as necessary
            new_energy = outside_score(new_puzzle)[0]
            if new_energy > max_score:
                max_puzzle = new_puzzle
                max_score = new_energy
            # decide whether to accept the new state
            if acceptance_probability(current_energy, new_energy, temperature) > random.random():
                current_puzzle = new_puzzle
                current_energy = new_energy
        # cool down the temperature
        temperature *= COOLING_RATE
    # print the final best puzzle found
    print(f"FINAL: {max_puzzle=}, {max_score=}")
    # compare this puzzle to a hill climbed version of it, and update maxes as needed
    check_max_puzzle = hill_climb(max_puzzle)
    if max_puzzle != check_max_puzzle:
        new_score = outside_score(check_max_puzzle)[0]
        if new_score > max_score:
            print(f"HILL CLIMB: {check_max_puzzle}, {new_score}")
            max_puzzle = check_max_puzzle
            max_score = new_score
    # update final maxes across the entire program as needed
    if max_score > final_score:
        final_score = max_score
        final_puzzle = max_puzzle
    # return the last found puzzle (not necessarily the highest one found)
    return current_puzzle

# run simulated annealing repeatedly
def main():
    current_puzzle = generate_initial_puzzle()
    for i in range(10000):
        # run sa on its own result
        current_puzzle = simulated_annealing(current_puzzle)
        if i%10 == 0:
            print(f"ALL-TIME {i}: {final_puzzle=}, {final_score=}")

if __name__=="__main__":
    main()