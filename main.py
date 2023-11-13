import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))

from config import *
from Population import Population
from RandomMutator import RandomMutator
from utils import evaluate_candidate_fitness

# Create and evolve the population
population = Population(
    size=population_size,
    fitness_function=evaluate_candidate_fitness,
    mutator=RandomMutator()
)

# Evolve the population and find the best candidate
best_candidate = population.evolve(generations=generations, visualize=True)

# Print the best candidate's actions and fitness
print("Best candidate actions:", best_candidate.actions)
print("Best candidate fitness:", best_candidate.fitness)
print("Tried to match:", target)
