from game_logic import *
import numpy as np

POPULATION_SIZE = 50


def fitness_function(points, moves):
    '''
    Funkcja celu
    '''
    return points**2 / (moves + 1)


def selection(fitness_functions, old_population):
    '''
    Selekcja algorytmu genetycznego
    '''
    fit = np.array(fitness_function)
    fit /= sum(fit)
    fit = np.cumsum(fit)

    new_population = []
    for _ in range(POPULATION_SIZE):
        rand = np.random.random()
        indx = np.where(fit == fit[fit >= rand][0])[0][0]
        new_population.append(old_population[indx])

    return new_population


def crossing():
    pass


def mutation():
    pass


population = [Game_logic() for _ in range(POPULATION_SIZE)]
