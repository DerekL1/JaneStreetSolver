# using tabu search, a modification of hill climbing that uses a tabu list to force exploration over exploitation to exceed the local optimum in regular hill climbing
# imports
from solver import outside_score
import random

# globals
global alphabet, iterations
alphabet = "ABCDEFGHIJKLMNOPRSTUVWXYZ"
iterations = 10000

# tabu search implementation
def tabu_search(initial_puzzle):
    # set up initial variables
    best_puzzle = current_puzzle = initial_puzzle
    best_score = outside_score(best_puzzle)[0]
    tabu_list = [best_puzzle]
    tabu_tenure = 25 # max length of tabu list
    
    for i in range(iterations):
        # create a set of all puzzles one letter alteration away from the current puzzle not in the tabu list
        neighbors = generate_neighbors(current_puzzle, tabu_list)

        # for all the valid neighbors find the one with the best score
        best_candidate = ""
        best_candidate_score = 0
        for candidate in neighbors:
            candidate_score = outside_score(candidate)[0]
            if candidate_score > best_candidate_score:
                best_candidate = candidate
                best_candidate_score = candidate_score
        
        # update the current puzzle
        current_puzzle = best_candidate
        
        # update the tabu list
        tabu_list.append(current_puzzle)
        if len(tabu_list) == tabu_tenure+1:
            tabu_list = tabu_list[1:]

        # update the global max if needed
        if best_candidate_score > best_score:
            best_puzzle = best_candidate
            best_score = best_candidate_score
        
    return best_puzzle

# creates a set of all valid neighbors
def generate_neighbors(puzzle, tabu_list):
    neighbors = set()
    # iterate through all the indices and letters
    for index in range(25):
        for letter in alphabet:
            if letter != puzzle[index]:
                new_puzzle = puzzle[:index]+letter+puzzle[index+1:]
                # ensure new puzzle is not in the tabu list
                if new_puzzle not in tabu_list:
                    neighbors.add(new_puzzle)
    return neighbors

# run tabu search on a random initial puzzle
def main():
    initial_puzzle = "".join([random.choice(alphabet) for i in range(25)])
    best_puzzle = tabu_search(initial_puzzle)
    print(f"{best_puzzle=}")

if __name__=="__main__":
    main()