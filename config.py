import random
import numpy as np

maximum_variation = 10 # Amount of possible "cultures" per position
max_seq_length = 10 # Maximum length of any sequence
target_length = 8 # Length of the target sequence

ACTIONS = ['action{}'.format(i) for i in range(1, maximum_variation)]
target = [random.choice(np.arange(3, maximum_variation)) for _ in range(target_length)]  # Randomly generate a target sequence

population_size = 250
generations = 200
