# given a puzzle, find all the valid states and achievements in it
# imports
import math
from collections import deque 

# declare global constants
global PUZZLE_LENGTH, PUZZLE_SQRT, MIN_SCORE
PUZZLE_LENGTH = 25
PUZZLE_SQRT = int(math.sqrt(PUZZLE_LENGTH))
MIN_SCORE = 165379868

# declare global variables
def set_globals(puzzle):
    global population_dict, neighbor_lookup, letter_lookup

    states = open("states.txt", "r")
    populations = open("populations.txt", "r")
    population_dict = {}
    for state, population in zip(states, populations):
        population_dict[state.replace("\n", "")] = int(population.replace("\n", ""))

    # create a lookup table of neighbors {index: (neighboring indices)}
    # and a lookup table of letters {letter: (corresponding indices)}
    neighbor_lookup = {}
    letter_lookup = {}
    for index in range(PUZZLE_LENGTH):
        neighbors = set()
        # left
        if index%PUZZLE_SQRT != 0:
            neighbors.add(index-1)
            # top left
            if index > PUZZLE_SQRT-1:
                neighbors.add(index-PUZZLE_SQRT-1)
            # bot left
            if index < PUZZLE_LENGTH-PUZZLE_SQRT:
                neighbors.add(index+PUZZLE_SQRT-1)
        # right
        if (index+1)%PUZZLE_SQRT != 0:
            neighbors.add(index+1)
            # top right
            if index > PUZZLE_SQRT-1:
                neighbors.add(index-PUZZLE_SQRT+1)
            # bot right
            if index < PUZZLE_LENGTH-PUZZLE_SQRT:
                neighbors.add(index+PUZZLE_SQRT+1)
        # top
        if index > PUZZLE_SQRT-1:
            neighbors.add(index-PUZZLE_SQRT)
        # bottom
        if index < PUZZLE_LENGTH-PUZZLE_SQRT:
            neighbors.add(index+PUZZLE_SQRT)
        neighbor_lookup[index] = neighbors
        # map letters in the puzzle to indices
        letter = puzzle[index]
        if letter in letter_lookup:
            letter_lookup[letter].add(index)
        else:
            letter_lookup[letter] = {index}
    # map unused letters in the puzzle to empty sets
    for character in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        if character not in letter_lookup:
            letter_lookup[character] = set()

# format puzzle and check if it is valid
def validate(puzzle):
    puzzle = puzzle.replace(" ", "")
    if len(puzzle) != PUZZLE_LENGTH:
        return ""
    if not puzzle.isalpha():
        return ""
    puzzle = puzzle.upper()
    set_globals(puzzle)
    return puzzle
    
# print a formatted layout of puzzle
def formatted_puzzle(puzzle):
    print("Submitted Puzzle: ")
    for i in range(PUZZLE_SQRT):
        print(puzzle[i*PUZZLE_SQRT: (i+1)*PUZZLE_SQRT])
    print("\t")

# breadth first search for the C2C achievement
def bfs(state_list):
    # create a bordering states dictionary for the states in the current puzzle
    border_lookup = {}
    borders = open("borders.txt", "r")
    for border in borders:
        border = border.replace("\n", "")
        border_list = border.split(" ")
        border_lookup[border_list[0]] = set(border_list[1:]).intersection(set(state_list))
    # using the stricter definition of east coast; only states that border the atlantic ocean (i.e. not Pennsylvania, Vermont, or West Virignia)
    east_coast = {"CONNECTICUT", "DELAWARE", "FLORIDA", "GEORGIA", "MAINE", "MARYLAND", "MASSACHUSETTS", "NEWHAMPSHIRE", "NEWJERSEY", "NEWYORK", "NORTHCAROLINA", "RHODEISLAND", "SOUTHCAROLINA", "VIRGINIA"}
    west_coast = {"WASHINGTON", "OREGON", "CALIFORNIA"}
    visited_start_states = set()
    for start_state in west_coast:
        visited = visited_start_states
        queue = deque([start_state])
        while queue:
            new_state = queue.popleft()
            if new_state not in visited:
                visited.add(new_state)
                if new_state in east_coast:
                    return True
                queue.extend(border_lookup[new_state])
        visited_start_states.add(start_state)
    return False

# check the points and achievements generated from the puzzle
def achievements(state_list):
    achievement_list = []
    points = m_count = c_count = 0
    for state in state_list:
        points += population_dict[state]
        if state[0] == "M":
            m_count += 1
        if state in {"COLORADO", "UTAH", "ARIZONA", "NEWMEXICO"}:
            c_count += 1
    # points from population counts
    achievement_list.append(points)
    # 20S: visits at least 20 states
    if len(state_list) >= 20:
        achievement_list.append("20S")
    # 200M: scores at least 200 million
    if points >= 200000000:
        achievement_list.append("200M")
    # PA: visits Pennsylvania
    if "PENNSYLVANIA" in state_list:
        achievement_list.append("PA")
    # M8: contains all 8 states that begin with an M
    if m_count == 8:
        achievement_list.append("M8")
    # 4C: contains the “Four Corners” states
    if c_count == 4:
        achievement_list.append("4C")
    # NOCAL: avoids California
    if "CALIFORNIA" not in state_list:
        achievement_list.append("NOCAL")
    # C2C: coast to coast
    if bfs(state_list):
        achievement_list.append("C2C")
    return achievement_list

# find the score and states in the puzzle
def score(puzzle):
    # iterate through all the states
    confirmed_states, raw_states = [], []
    for state in population_dict:
        first_letter = state[0]
        outcome = ""
        # iterate through all the indices starting with the first letter of the state and recurse
        for index in letter_lookup[first_letter]:
            outcome = find_state(puzzle, state, first_letter, index, True)
            if outcome: break
        # if state is not found, start with an alternate letter, iterating through all the other indices and recursing
        if not outcome:
            for index in range(PUZZLE_LENGTH):
                if index not in letter_lookup[first_letter]:
                    outcome = find_state(puzzle, state, puzzle[index], index, False)
                if outcome: break
        # if state is found, add the raw and the original state to saved lists
        if outcome: 
            raw_states.append(outcome)
            confirmed_states.append(state)
    # if states are found, list them out and return the achievements generated
    if confirmed_states:
        output_string = f"Congrats! You found {len(confirmed_states)} states:\n"
        for state in population_dict:
            if state in confirmed_states:
                i = confirmed_states.index(state)
                if (raw_states[i] == confirmed_states[i]):
                    output_string += confirmed_states[i] + ", "
                else:
                    output_string += confirmed_states[i] + f" ({raw_states[i]}), "
        output_string = output_string[:-2]
        print(output_string)
        return achievements(confirmed_states)
    else:
        print("Sorry, you found no states.")
        return [0]

# recurse through the puzzle to see if the state is there
def find_state(puzzle, state, unfinished_state, index, alternate):
    # base case: if a final puzzle state is reached return current string
    if len(unfinished_state) == len(state):
        return unfinished_state
    # find the list of possible indices that the next letter in the state can be at
    next_letter = state[len(unfinished_state)]
    neighbor_letters = letter_lookup[next_letter].intersection(neighbor_lookup[index])
    # iterate through that list and recurse down the neighboring indices
    for next_index in neighbor_letters:
        final_state = find_state(puzzle, state, unfinished_state+next_letter, next_index, alternate)
        if len(final_state) == len(state):
            return final_state
    # if a final state is not reached and the alternate letter can still be used
    if alternate:
        # iterate through all the other neighbors around the current index and recurse without an alternate letter
        neighbor_letters = neighbor_lookup[index] - letter_lookup[next_letter]
        for next_index in neighbor_letters:
            final_state = find_state(puzzle, state, unfinished_state+puzzle[next_index], next_index, False)
            if len(final_state) == len(state):
                return final_state
    # if a final state is still not reached, abandon this path
    return ""

# score function used for other programs
def outside_score(puzzle):
    global PUZZLE_LENGTH, PUZZLE_SQRT
    PUZZLE_LENGTH = len(puzzle)
    PUZZLE_SQRT = int(math.sqrt(PUZZLE_LENGTH))
    set_globals(puzzle)
    confirmed_states, raw_states = [], []
    for state in population_dict:
        first_letter = state[0]
        outcome = ""
        for index in letter_lookup[first_letter]:
            outcome = find_state(puzzle, state, first_letter, index, True)
            if outcome: break
        if not outcome:
            for index in range(PUZZLE_LENGTH):
                if index not in letter_lookup[first_letter]:
                    outcome = find_state(puzzle, state, puzzle[index], index, False)
                if outcome: break
        if outcome: 
            raw_states.append(outcome)
            confirmed_states.append(state)
    return achievements(confirmed_states)

# main method to allow user input for one puzzle
def main(): 
    puzzle = input("Enter your puzzle: ")
    puzzle = validate(puzzle)
    if validate(puzzle):
        formatted_puzzle(puzzle)
        final_score = score(puzzle)
        if final_score[0] >= MIN_SCORE:
            print(f"Congratulations! You have qualified for the leaderboard with a score of {final_score[0]}")
            if len(final_score) > 1:
                retString = "You have also achieved the following awards: "
                for index in range(1, len(final_score)):
                    retString += final_score[index] + ", "
                retString = retString[:-2]
                print(retString)
        else:
            print(f"Unfortunately, your puzzle with a score of {final_score[0]} points did not meet the minimum required score ({MIN_SCORE}) to qualify for the leaderboards.")
            if len(final_score) > 1:
                retString = "However, you achieved the following awards: "
                for index in range(1, len(final_score)):
                    retString += final_score[index] + ", "
                retString = retString[:-2]
                print(retString)
    else:
        print("Invalid puzzle entered")

if __name__=="__main__": 
    main() 