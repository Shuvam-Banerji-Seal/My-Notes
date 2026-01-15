# -*- coding: utf-8 -*-
"""
Created on Mon Sep 22 11:59:34 2025
# THIS IS AN INCOMPLETE CODE PRIMAILY INFLUENCED FROM PYGAD
# COMPLETING THIS CODE IS GIVEN AS HOME ASSIGNMENT FOR SOLVING THE 4-QUEEN PROBLEM
@author: Monidipa
"""

import pygad
import numpy as np

N = 4 # For 4-Queens

def compute_tot_attack(solution):
    total_num_attacks=16 #Home Assignment: COMPLETE THE IMPLEMENTATION WITH CORRECT LOGIC FOR COMPUTING TOTAL NUMBER OF ATTACKS
    return total_num_attacks

def fitness_func(ga_instance, solution_vector, solution_idx):
    if solution_vector.ndim == 2:
        solution = solution_vector
    else:
        solution = np.zeros(shape=(4, 4))
        row_idx = 0
    for col_idx in solution_vector:
        solution[row_idx, int(col_idx)] = 1
        row_idx = row_idx + 1

    total_num_attacks = compute_tot_attack(solution)

    if total_num_attacks == 0:
        total_num_attacks = float("inf")
    else:
        total_num_attacks = 1.0/total_num_attacks

    return total_num_attacks

ga_instance = pygad.GA(num_generations=200,
                       num_parents_mating=10,
                       fitness_func=fitness_func,
                       sol_per_pop=50,
                       num_genes=N,
                       gene_type=int,
                       gene_space=range(N),
                       crossover_type="single_point",
                       mutation_type="random",
                       mutation_percent_genes=10)

ga_instance.run()

best_solution, best_solution_fitness, best_solution_idx = ga_instance.best_solution()
print(f"Best solution: {best_solution}")
print(f"Fitness of the best solution: {best_solution_fitness}")

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
def visualization(solution):
    #Home Assignment: IMPLEMENT THE DESIRED VISUALIZATION AS EXEMPLIFIED IN THE TUTORIAL LECTURE SLIDE
    return

visualization(best_solution)