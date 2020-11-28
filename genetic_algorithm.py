from game_logic import *
import numpy as np
from tqdm import tqdm


class GeneticAlgorithm:
    def __init__(self, population_size=50, max_generation=100, save_points=True, save_move_count=False, save_fitness_function=False, save_weights=False):
        '''
        Algorytm genetyczny
        '''
        self.population_size = population_size
        self.max_generation = max_generation
        self.save_points = save_points
        self.save_move_count = save_move_count
        self.save_fitness_function = save_fitness_function
        self.save_weights = save_weights
        self.generation_points = []  # Ile punktów zdobyła dana generacja
        self.generation_move_count = []  # Ile kroków wykonała dana generacja
        self.generation_fitness_function = []  # Ile wynosiła funkcja dopasowania dla danej generacji
        self.generation_weights = []  # Zapisane wagi osobników z poszczególnych generacji

        self.population = [Game_logic() for _ in range(self.population_size)]

        for _ in tqdm(range(self.max_generation)):
            self.evolve_population()

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
            indx = np.argmax(fit >= rand)
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

            if indx1 < indx2:
                genotype1, genotype2 = genotypes.pop(indx1), genotypes.pop(indx2-1)
            else:
                genotype1, genotype2 = genotypes.pop(indx1), genotypes.pop(indx2)

            crossing_indx = np.random.randint(len(genotype1))
            genotype1[:crossing_indx], genotype2[:crossing_indx] = genotype2[:crossing_indx], genotype1[:crossing_indx]

            new_genotypes.append(genotype1)
            new_genotypes.append(genotype2)

        return new_genotypes

    def mutation(self, genotype, probability=1/100):
        '''
        Mutacja pojedynczego genotypu z
        ustalonym prawdopodobienstwem.
        Genotyp powinien być płaską tablicą 1D
        '''
        for indx in range(len(genotype)):
            rand = np.random.random()
            if rand < probability:
                genotype[indx] = np.random.uniform(-1, 1)

        return genotype

    def evolve_population(self):
        '''
        Pojedyncza ewolucja całej populacji
        '''
        # Selekcja
        fitness_functions = [self.fitness_function(*game_logic.run_game()) for game_logic in self.population]
        new_population_weights = self.selection(fitness_functions)

        # Zapisanie wag poprzedniej generacji
        if self.save_weights:
            self.generation_weights.append([game_logic.get_neural_weights() for game_logic in self.population])

        # Krzyżowanie
        new_population_weights = list(map(self.flatten_weights, new_population_weights))
        new_population_weights = self.crossing(new_population_weights)

        # Mutacja
        new_population_weights = list(map(self.mutation, new_population_weights))

        # Zapisanie punktów i kroków wykonanych przez osobników z tej generacji
        if self.save_points:
            self.generation_points.append([game_logic.get_points() for game_logic in self.population])
        if self.save_move_count:
            self.generation_move_count.append([game_logic.get_move_count() for game_logic in self.population])
        if self.save_fitness_function:
            self.generation_fitness_function.append(fitness_functions)

        # Nadanie poprawnych wymiarów wagom i przypisanie ich osobnikom
        new_population_weights = [self.unflatten_weights(flat_weights) for flat_weights in new_population_weights]
        for new_weight, game_logic in zip(new_population_weights, self.population):
            game_logic.set_neural_weights(new_weight)
            game_logic.clear()

    def get_generations_points(self):
        '''
        Zwraca tablicę z punktami zdobytymi przez 
        każdego z osobników z danej generacji
        '''
        return self.generation_points

    def get_generations_move_count(self):
        '''
        Zwraca tablicę z krokami wykonanymi przez 
        każdego z osobników z danej generacji
        '''
        return self.generation_move_count

    def get_best_snake(self, print_timeout=False):
        '''
        Zwraca węża który zdobędzie najwięcej punktów z obecnej populacji
        '''
        points = []
        for game_logic in self.population:
            pts, moves = game_logic.run_game()
            points.append(pts)
            game_logic.clear(print_timeout)

        indx = np.argmax(points)
        return self.population[indx]
