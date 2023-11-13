from config import *

from typing import List

def evaluate_candidate_fitness(candidate_actions: List[str]) -> float:
    candidate_actions = encode_context(candidate_actions)

    # Calculate the common length
    common_length = min(len(candidate_actions), len(target))
    
    # Calculate the initial distance based on the difference in length
    distance = abs(len(candidate_actions) - len(target))
    
    # Compare elementwise for the common length of the sequences
    for idx in range(common_length):
        if candidate_actions[idx] != target[idx]:
            distance += 1
    
    return distance

def encode_context(candidate_actions: List[str]) -> List[int]:
    return [ACTIONS.index(action) + 1 for action in candidate_actions if action in ACTIONS]


# def encode_context(candidate_actions: List[str]) -> List[int]:
#     # One-hot encode the actions into a matrix, then flatten it
#     encoded_matrix = [[0] * max_seq_length for _ in range(len(ACTIONS))]
#     for i, action in enumerate(candidate_actions):
#         if i < max_seq_length:
#             action_index = ACTIONS.index(action)
#             encoded_matrix[action_index][i] = 1
#     encoded_vector = [item for sublist in encoded_matrix for item in sublist]
#     return encoded_vector