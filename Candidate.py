import os
import random
from typing import Callable

os.chdir(os.path.dirname(os.path.realpath(__file__)))

from config import *
from utils import evaluate_candidate_fitness

class Candidate:
    def __init__(self, actions=None, mutator=None):
        if actions is not None:
            self.actions = actions
        else:
            # Ensure at least two actions are added initially
            initial_action_count = random.randint(2, max_seq_length//2)
            self.actions = random.sample(ACTIONS, k=initial_action_count)
        self.mutator = mutator
        self.previous_fitness = None
        self.fitness = evaluate_candidate_fitness(self.actions)

    def add_action(self, index, action):
        """ Adds the specified action to the candidate's actions at the specified index. """
        if index <= len(self.actions):
            self.actions.insert(index, action)
        else:
            print(f"Warning: Attempted to add action at index {index}, which is out of bounds.")


    def remove_action(self, index):
        """ Removes an action from the candidate's actions at the specified index. """
        if 0 <= index < len(self.actions):
            self.actions.pop(index)
        else:
            print(f"Warning: Attempted to remove action at index {index}, which is out of range for current actions.")

    def permute_actions(self, index1, index2):
        """ Switches two actions in the candidate's actions at the specified indices. """
        if 0 <= index1 < len(self.actions) and 0 <= index2 < len(self.actions):
            self.actions[index1], self.actions[index2] = self.actions[index2], self.actions[index1]
        else:
            print(f"Warning: Attempted to permute actions at indices {index1} and {index2}, which are out of range for current actions.")
    
    def mutate(self, mutation_type, *indices, action):
        # Flatten the tuple if it's nested
        indices = indices if isinstance(indices[0], int) else indices[0]

        if mutation_type == 1:
            if action != 0:  # Ensure we're not adding a 'no action'
                index = indices[0]
                self.add_action(index, action)
            else:
                raise ValueError("Warning: Attempted to add a 'no action'.")
        elif mutation_type == 2:
            index = indices[0]
            self.remove_action(index)
        elif mutation_type == 3:
            index1, index2 = indices
            self.permute_actions(index1, index2)
        else:
            raise ValueError(f"Invalid mutation type {mutation_type} of type {type(mutation_type)}")



    def evaluate_fitness(self, fitness_function: Callable):
        """ Evaluates the candidate's fitness using the provided fitness function. """
        # Only update previous_fitness if fitness has already been set.
        if hasattr(self, 'fitness'):
            self.previous_fitness = self.fitness
        self.fitness = fitness_function(self.actions)
        return self.fitness