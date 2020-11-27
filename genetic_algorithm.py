from game_logic import *
import numpy as np


class GeneticAlgorith:
    def __init__(self, population_size=50, max_generation=100):
        '''
        Algorytm genetyczny
        '''
        self.population_size = population_size
        self.max_generation = max_generation

        self.population = [Game_logic() for _ in range(self.population_size)]

    def fitness_function(self, points, move_count):
        '''
        Funkcja przystosowania osobnika
        '''
        return points**2 / (1 + move_count)

    def flatten_weights(weights):
        '''
        Zwija wagi sieci neuronowej do tablicy 1D
        '''
        weights1, weights2 = weights
        return np.hstack(weights1, weights2)

    def unflatten_weights(weights):
        '''
        Rozwija wagi sieci neuronowej formatu oczekiwanego przez sieć
        '''
        weights1, weights2 = weights[:4*6], weights[4*6:]
        weights1.reshape((4, 6))
        weights2.reshape((6, 3))
        return [weights1, weights2]

    def selection(self, fitness_functions):
        '''
        Przyjmując wartości fitness_functions wybiera
        ruletką osobniki do kolejnej populacji
        '''
        fit = np.array(fitness_functions)
        fit = np.divide(fit, np.sum(fit))
        fit = np.cumsum(fit)

        new_genotypes = []
        for _ in range(self.population_size):
            rand = np.random.random()
            indx, = np.where(fit == fit[fit >= rand][0])[0]
            new_genotypes.append(self.population[indx].get_neural_weights)

        return new_genotypes

    def crossing(self, genotypes: list):
        '''
        Krzyżowanie osobników populacji
        Genotypy powinny być płaskimi tablicami 1D
        '''
        new_genotypes = []

        '''
        Pętla losująca dwa osobniki, a następnie je krzyżująca
        Skrzyżowane osobniki są dodawane do new_genotypes
        '''
        while len(genotypes) > 0:
            indx1, indx2 = np.random.randint(len(genotypes), size=2)
            while indx1 == indx2:
                indx2 = np.random.randint(len(genotypes))

            genotype1, genotype2 = genotypes.pop(indx1), genotypes.pop(indx2-1)

            crossing_indx = np.random.randint(len(genotype1))
            genotype1[:crossing_indx], genotype2[:crossing_indx] = genotype2[:crossing_indx], genotype1[:crossing_indx]

            new_genotypes.append(genotype1)
            new_genotypes.append(genotype2)

        return new_genotypes

    def mutation(self, genotype, probability=1/1000):
        '''
        Mutacja pojedynczego genotypu z
        ustalonym prawdopodobienstwem.
        Genotyp powinien być płaską tablicą 1D
        '''
        for indx in range(len(genotype)):
            rand = np.random.random()
            if rand < probability:
                genotype[indx] = np.random.random()

        return genotype

    def evolve_population(self):
        pass
