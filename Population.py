import matplotlib.pyplot as plt
import csv
from typing import List, Callable, Any

from config import *
from Candidate import Candidate
from utils import encode_context

class Population:
    def __init__(self, size: int, fitness_function: Callable, mutator):
        self.candidates = [Candidate(mutator=mutator) for _ in range(size)]
        self.fitness_function = fitness_function
        self.mutator = mutator
        self.max_seq_length = max_seq_length
        self.evolution_record = []  # To record the evolution process
    
    def select_parents(self):
        # Helper function to select one parent
        def select_one_parent(exclude_candidate=None):
            # Calculate the total fitness excluding the candidate to be excluded
            total_fitness = sum(c.fitness for c in self.candidates if c != exclude_candidate)
            
            # If there's no fitness left after exclusion, there's an issue with the exclusion logic or fitness distribution
            if total_fitness <= 0:
                raise ValueError("Total fitness is non-positive after exclusion. Check the exclusion logic and fitness values.")

            # Generate a random selwrite_evolution_to_csvection point
            selection_point = random.uniform(0, total_fitness)
            current = 0

            for candidate in self.candidates:
                # Skip the excluded candidate if specified
                if candidate == exclude_candidate:
                    continue

                current += candidate.fitness
                # If we've reached the selection point, return the current candidate
                if current > selection_point:
                    return candidate

            # If no candidate is selected, which should not happen, raise an error
            raise RuntimeError("Selection failed: no candidate was selected.")

        # Select the first parent
        parent1 = select_one_parent()
        # Select the second parent, ensuring it's different from the first
        parent2 = None
        try:
            parent2 = select_one_parent(exclude_candidate=parent1)
        except RuntimeError:
            # Handle the case where no second parent could be selected
            # This could involve retrying with a different logic, logging the error, etc.
            print("An error occurred while selecting the second parent. Handling the case appropriately.")

        # Ensuring that parent2 is selected and is different from parent1
        while parent2 is None or parent1 is parent2:
            try:
                parent2 = select_one_parent(exclude_candidate=parent1)
            except RuntimeError:
                # Handle the case where no second parent could be selected
                # This could involve retrying with a different logic, logging the error, etc.
                print("An error occurred while re-selecting the second parent. Handling the case appropriately.")

        return parent1, parent2
    
    def reproduce(self, parent1, parent2):
        # Determine the crossover point
        if len(parent1.actions) < 2 or len(parent2.actions) < 2:
        # Handle the insufficient actions case
            raise ValueError("One of the parents does not have enough actions for crossover.")
        
        crossover_point = random.randint(1, min( len( parent1.actions ), len( parent2.actions ) ) - 1 )

        # Create the offspring by combining the actions
        child1_actions = parent1.actions[:crossover_point] + parent2.actions[crossover_point:]
        child2_actions = parent2.actions[:crossover_point] + parent1.actions[crossover_point:]

        # Create Candidate instances for the offspring
        child1 = Candidate(actions=child1_actions)
        child2 = Candidate(actions=child2_actions)

        return child1, child2


    def evolve(self, generations: int, visualize=False):
        # Initialize visualization
        if visualize:
            plt.ion()  # Turn on interactive mode
            fig, ax = plt.subplots()
            ax.set_xlim(0, generations)
            ax.set_ylim(0, 10)  # Assuming the fitness score range is known
            ax.set_xlabel('Generation')
            ax.set_ylabel('Fitness')
            line_max, = ax.plot([], [], 'r-', label='Max Fitness')
            line_avg, = ax.plot([], [], 'g-', label='Average Fitness')
            line_min, = ax.plot([], [], 'b-', label='Min Fitness')
            plt.legend()
            plt.title('Evolution of Fitness Over Generations')
            plt.show()

        fitness_stats = {'max': [], 'avg': [], 'min': []}
        for generation in range(generations):
            # Fitness evaluation for each candidate
            for candidate in self.candidates:
                candidate.fitness = self.fitness_function(candidate.actions)

            # New generation container
            new_generation = []

            # Reproduction process
            while len(new_generation) < len(self.candidates):
                # Selection process - Select two different parents for each new offspring
                parent1, parent2 = self.select_parents()

                # Create two new offspring from the selected parents
                child1, child2 = self.reproduce(parent1, parent2)
                
                # Add the new offspring to the new generation
                new_generation.extend([child1, child2])

            # If the reproduction creates more candidates than the original population size, trim the new generation
            self.candidates = new_generation[:len(self.candidates)]


            for candidate in self.candidates:
                old_actions = candidate.actions.copy()  # Assuming you need a copy of the original state
                mutation_info = self.mutator.decide_mutation(candidate.actions)
                mutation_type = mutation_info[0]
                action = mutation_info[1]
                indices = mutation_info[2:]
                candidate.mutate(mutation_type, *indices, action = action)
                new_actions = candidate.actions  # Assuming actions have now changed due to mutation
                new_fitness = self.fitness_function(candidate.actions)
                fitness_change = new_fitness - candidate.fitness

                # Now we construct the mutation record
                mutation_record = {
                    'old_state': old_actions,
                    'action': action,
                    'mutation_type': mutation_type,
                    'indices': indices,
                    'fitness_change': fitness_change
                }
                self.mutator.record_mutation(mutation_record)

            # Train the smarter mutator models
            self.mutator.train_models()

            # Visualization update
            if visualize:
                fitness_scores = [c.fitness for c in self.candidates]
                fitness_stats['max'].append(max(fitness_scores))
                fitness_stats['avg'].append(sum(fitness_scores) / len(fitness_scores))
                fitness_stats['min'].append(min(fitness_scores))

                line_max.set_data(range(generation + 1), fitness_stats['max'])
                line_avg.set_data(range(generation + 1), fitness_stats['avg'])
                line_min.set_data(range(generation + 1), fitness_stats['min'])
                ax.set_xlim(0, generation + 1)
                # Adjust the y-axis dynamically based on max fitness
                ax.set_ylim(0, max(fitness_stats['max']) * 1.1)
                plt.pause(0.01)  # Pause for 0.01 seconds to update the plot and allow inspection

                if generation == generations - 1:
                    plt.show(block=True)

        # Return the candidate with the highest fitness
        best_candidate = min(self.candidates, key=lambda x: x.fitness)
        return best_candidate
