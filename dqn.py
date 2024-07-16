# using deep q networks, a form of reinforcement learning to train an agent to make optimal choices given a board state
# imports
import random
import numpy as np
import tensorflow as tf
from collections import deque
from solver import outside_score

# globals
global ALPHABET
ALPHABET = "ABCDEFGHIJKLMNOPRSTUVWXYZ"

# class to represent the puzzle board
class PuzzleEnvironment:
    #default constructor sets up random puzzle
    def __init__(self):
        self.puzzle = "".join([random.choice(ALPHABET) for i in range(25)])

    # updates the puzzle to reflect the action given, and returns new puzzle and reward
    def step(self, action):
        # changes action from number [0, 625) to an index [0, 25) and letter [A-Z] except Q
        new_index = action // 25
        new_letter = ALPHABET[action % 25]
        # updates the puzzle
        new_puzzle = list(self.puzzle)
        new_puzzle[new_index] = new_letter
        self.puzzle = ''.join(new_puzzle)
        reward = self._calculate_reward()
        return self.puzzle, reward

    # calculates the current reward of puzzle
    def _calculate_reward(self):
        return outside_score(self.puzzle)[0]

    # resets puzzle to new random puzzle and returns that
    def reset(self):
        self.puzzle = "".join([random.choice(ALPHABET) for i in range(25)])
        return self.puzzle

# class to represent the deep q learning agent
class DQNAgent:
    # default constructor takes a puzzle and action size and sets up learning constants
    def __init__(self, puzzle_size, action_size):
        self.puzzle_size = puzzle_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)  # replay memory
        self.gamma = 0.95  # discount factor
        self.epsilon = 1.0  # exploration-exploitation trade-off
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()

    # create keras model
    def _build_model(self):
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(32, input_dim=self.puzzle_size, activation='relu'),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(self.action_size, activation='linear')
        ])
        model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam())
        return model

    # add an action and its impact on reward and puzzle to memory
    def remember(self, puzzle, action, reward, new_puzzle):
        self.memory.append((puzzle, action, reward, new_puzzle))

    # function to choose what action to take given a puzzle
    def choose_action(self, puzzle):
        # if random number from 0 to 1 is less than epsilon, explore the solution space and take a random action
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        # otherwise, take the models best predicted action
        else:
            q_values = self.model.predict(np.array([puzzle]), verbose=0)[0]
            return np.argmax(q_values)

    # replay function to allow model to reuse previous learning and combat forgetting
    def replay(self, batch_size):
        # if there is not enough memory for a single batch, exit
        if len(self.memory) < batch_size:
            return
        # generate a random batch from the memory
        minibatch = random.sample(self.memory, batch_size)
        for puzzle, action, reward, new_puzzle in minibatch:
            # calculate the new target from the reward given from the action of the puzzle and the predicted max reward from the new puzzle times a discount factor
            target = reward + self.gamma * np.amax(self.model.predict(np.array([new_puzzle]), verbose=0)[0])
            # re-fit the model for the given puzzle to reflect the new target
            target_f = self.model.predict(np.array([puzzle]), verbose=0)
            target_f[0][action] = target
            self.model.fit(np.array([puzzle]), target_f, epochs=1, verbose=0)
        # decay the exploration factor (epsilon) if it is above the minimum
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

# main method to run agent training and apply it
def main():
    # set up puzzle and agent constants
    env = PuzzleEnvironment()
    puzzle_size = 25  # total number of letters in the puzzle
    action_size = 625  # number of possible actions (25 indices * 25 letters)
    agent = DQNAgent(puzzle_size, action_size)
    batch_size = 32
    num_episodes = 1000
    num_actions = 1000

    # set up puzzle maxes
    max_reward = 0
    max_puzzle = ""

    # iterate through training episodes
    for episode in range(num_episodes):
        if episode%50 == 0:
            print(f"{episode=}")
            print(f"{max_puzzle=}, {max_reward=}")
        # reset the puzzle
        puzzle = env.reset()
        for i in range(num_actions):
            puzzle_vector = np.array([ord(c) for c in puzzle]) # convert letters to numerical representation if needed
            # choose the action and update the puzzle and reward
            action = agent.choose_action(puzzle_vector)
            new_puzzle, reward = env.step(action)
            new_puzzle_vector = np.array([ord(c) for c in new_puzzle]) # convert the neww puzzle into numbers too
            # commit the puzzles, reward, and action to memory
            agent.remember(puzzle_vector, action, reward, new_puzzle_vector)
            # update puzzle and maximums as needed
            puzzle = new_puzzle
            if reward > max_reward:
                max_puzzle = new_puzzle
                max_reward = reward
                # print(f"{max_puzzle=}, {max_reward=}")
        # replay after each episode
        agent.replay(batch_size)

    # after training, apply the agent to a puzzle
    print(f"AFTER TRAINING: {max_puzzle=}, {max_reward=}")
    # reset the puzzle and maximums
    max_puzzle = ""
    max_reward = 0
    puzzle = env.reset()
    # repeatedly iterate through the puzzle using the agent to make moves
    while True:
        # convert puzzle into numerical form
        puzzle_vector = np.array([ord(c) for c in puzzle])
        # choose best action determined by agent for given puzzle and apply it
        action = agent.choose_action(puzzle_vector)
        puzzle, reward = env.step(action)
        # if maximum needs updating, do it
        if reward > max_reward:
            max_puzzle = puzzle
            max_reward = reward
            print(f"{max_puzzle=}, {max_reward=}")

if __name__=="__main__":
    main()