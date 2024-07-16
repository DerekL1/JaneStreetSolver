# using hill climbing, an algorithm to find the deterministic local optimum of a puzzle
# imports
from solver import outside_score
import random

# set up globals
global alphabet
alphabet = "ABCDEFGHIJKLMNOPRSTUVWXYZ"

# custom holistic scoring method that adds points for achievements
def holistic_score(puzzle):
    achievements = outside_score(puzzle)
    total_score = achievements[0]
    total_mult = 1
    # set up individual weights as wanted
    for i in range(1, len(achievements)):
        award = achievements[i]
        if award == "20S":
            total_mult += 0
        if award == "200M":
            total_mult += 0
        if award == "PA":
            total_mult += 0
        if award == "M8":
            total_mult += 0
        if award == "4C":
            total_mult += 0
        if award == "NOCAL":
            total_mult += 0
        if award == "C2C":
            total_mult += 0
    return total_score*total_mult

# strict hill climbing method
def hill_climb(puzzle):
    # set a local max score and puzzle to keep track inside the current iteration
    max_score = -1
    prev_ind = -1
    prev_score = -2
    while max_score > prev_score:
        prev_score = max_score
        max_score = -1
        max_puzzle = ""
        # check what changing each letter would do
        # iterate through the indices of the puzzle
        for i in range(len(puzzle)):
            # if the target index was not the last changed index, iterate through each letter of the alphabet
            if not i == prev_ind:
                for letter in alphabet:
                    #calculate the new score if the letter changes at the index and update as needed
                    if not puzzle[i] == letter:
                        temp_score = outside_score(puzzle[:i]+letter+puzzle[i+1:])[0]
                        if temp_score > max_score:
                            # set new max score and puzzle
                            max_score = temp_score
                            max_puzzle = puzzle[:i]+letter+puzzle[i+1:]
                            # keep track of which index was changed
                            prev_ind = i
            # check what swapping letters would do
            for j in range(i+1, len(puzzle)):
                temp_puzzle = puzzle[:i]+puzzle[j]+puzzle[i+1:j]+puzzle[i]+puzzle[j+1:]
                temp_score = outside_score(temp_puzzle)[0]
                if temp_score > max_score:
                    max_score = temp_score
                    max_puzzle = temp_puzzle
                    prev_ind = -1
        puzzle = max_puzzle
    return puzzle

# hill climbing with resetting
def main():
    # can change the raw puzzle depending on desired starting letter frequency
    raw_puzzle = alphabet

    hill_climbs = 100 # no. of times to iterate through hill climbing
    resets = 1000 # no. of random puzzles generated at the reset point when hill climbing stagnates

    # set up the initial puzzle, using a randomly generated pattern of the raw letter frequency in raw_puzzle
    init_puzzle = ''.join(random.sample(raw_puzzle, 25))
    init_score = holistic_score(init_puzzle)
    # set up global maxes for score and puzzle
    final_puzzle = ""
    final_score = -1
    # set up previous variables to ensure the hill climbing does not stagnate
    prev_ind = -1
    prev_score = -1

    # loop through the hill climbing process
    for loop in range(hill_climbs):
        # set a local max score and puzzle to keep track inside the current iteration
        max_score = -1
        max_puzzle = ""
        # iterate through the indices of the puzzle
        for i in range(len(init_puzzle)):
            # if the puzzle was not the last changed index, iterate through each letter of the alphabet
            if not i == prev_ind and not init_puzzle[i] == "Y" and not init_puzzle[i] == "W":
                for letter in alphabet:
                    #calculate the new score if the letter changes at the index and update as needed
                    if not init_puzzle[i] == letter:
                        temp_score = holistic_score(init_puzzle[:i]+letter+init_puzzle[i+1:])
                        if temp_score > max_score:
                            # set new max score and puzzle
                            max_score = temp_score
                            max_puzzle = init_puzzle[:i]+letter+init_puzzle[i+1:]
                            # keep track of which index was changed
                            prev_ind = i
        # if local max beats global max, update
        if max_score > final_score:
            final_score = max_score
            final_puzzle = max_puzzle
        # if local max beats previous iteration's max, set local as new starting point
        if max_score > prev_score:
            init_puzzle = max_puzzle
            init_score = max_score
            prev_score = init_score
        # if local max does not improve, reset the starting point
        else:
            init_puzzle = ""
            init_score = -1
            # generate a new random puzzle using the same letter frequency as this iteration's max
            for i in range(resets):
                puzzle = ''.join(random.sample(max_puzzle*2,len(max_puzzle)))
                score = holistic_score(puzzle)
                # keep track of the best puzzle
                if score > init_score:
                    init_score = score
                    init_puzzle = puzzle
            # if new starting puzzle beats old global max, update
            if init_score > final_score:
                final_score = init_score
                final_puzzle = init_puzzle
            prev_score = init_score

    print("FINAL:")
    print(final_puzzle)
    print(final_score)

if __name__=="__main__": 
    main()