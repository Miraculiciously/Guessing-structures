from abc import ABC, abstractmethod
from sklearn.preprocessing import OneHotEncoder
from typing import Any, Tuple
import random
from config import *

class Mutator(ABC):
    def __init__(self):
        super().__init__()
        self.encoder = OneHotEncoder(sparse=True)  # Global encoder

    def one_hot_encode(self, features):
        print(f"{features} is of type {type(features)}")
        # Convert features to a numpy array and reshape for the encoder
        features_array = np.array(features).reshape(-1, 1)
        encoded_features = self.encoder.fit_transform(features_array)
        return encoded_features

    def random_mutation(self, actions):
        actions_length = len(actions)
        possible_choices = [1, 2, 3]

        # Adjust possible choices based on actions_length and max_seq_length
        if actions_length <= 2:
            possible_choices = [1]
        elif actions_length >= max_seq_length:
            possible_choices.remove(1)

        choice = random.choice(possible_choices)
        index = self.choose_index(actions_length)
        second_index = None
        action = 0

        if choice == 3:  # permute_actions, need two different indices
            second_index = self.choose_index(actions_length, exclude_index=index)

        # Set action for add_action (choice 1)
        if choice == 1:  # add_action
            action = random.choice(ACTIONS)  # Assuming ACTIONS is defined elsewhere

        if second_index is None:
            return choice, action, (index,)
        else:
            return choice, action, (index, second_index)


    @staticmethod
    def choose_index(actions_length, exclude_index=None):
        indices = list(range(actions_length))
        if exclude_index is not None and exclude_index in indices:
            indices.remove(exclude_index)
        return random.choice(indices)

    @abstractmethod
    def decide_mutation(self, context: Any) -> Tuple[str, Tuple[int, ...]]:
        """
        Decides on the mutation to perform.
        :param context: The context in which to decide the mutation (e.g., the current actions of a candidate).
        :return: A tuple containing the mutation type and the indices involved.
        """
        pass

    @abstractmethod
    def train_models(self) -> None:
        """
        Trains the underlying models to better predict the effects of mutations.
        """
        pass
