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

    def flatten_weights(self, weights):
        '''
        Zwija wagi sieci neuronowej do tablicy 1D
        '''
        weights1, weights2 = weights
        return np.hstack((weights1.flatten(), weights2.flatten()))

    def unflatten_weights(self, weights):
        '''
        Rozwija wagi sieci neuronowej formatu oczekiwanego przez sieć
        '''
        weights1, weights2 = weights[:4*6], weights[4*6:]
        weights1 = np.reshape(weights1, (4, 6))
        weights2 = np.reshape(weights2, (6, 3))
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
            indx = np.argmax(fit >= rand)  # np.where(fit == fit[fit >= rand][0])[0][0]
            new_genotypes.append(self.population[indx].get_neural_weights())

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
        '''
        Pojedyncza ewolucja całej populacji
        '''
        # Selekcja
        fitness_functions = [self.fitness_function(*game_logic.run_game()) for game_logic in self.population]
        new_population_weights = self.selection(fitness_functions)

        # Krzyżowanie
        new_population_weights = list(map(self.flatten_weights, new_population_weights))
        new_population_weights = self.crossing(new_population_weights)

        # Mutacja
        new_population_weights = list(map(self.mutation, new_population_weights))

        # Nadanie poprawnych wymiarów wagom i przypisanie ich osobnikom
        new_population_weights = [self.unflatten_weights(flat_weights) for flat_weights in new_population_weights]
        for new_weight, game_logic in zip(new_population_weights, self.population):
            game_logic.set_neural_weights(new_weight)
            game_logic.clear()
