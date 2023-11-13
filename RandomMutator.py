import random
from typing import Tuple
from abstract_mutator import Mutator

class RandomMutator(Mutator):
    def __init__(self):
        super().__init__()  # Initialize the base class
        self.number_to_choice = {
            1: 'add_action',
            2: 'remove_action',
            3: 'permute_actions'
        }

    def decide_mutation(self, actions):
        return self.random_mutation(actions)

    def record_mutation(self, *args, **kwargs) -> None:
        # Placeholder implementation
        pass

    def train_models(self, *args, **kwargs) -> None:
        # Placeholder implementation
        pass