from genetic_algorithm import *
from game_logic import *


def main():
    algorithm = GeneticAlgorith(population_size=100)

    for _ in range(50):
        algorithm.evolve_population()

    algorithm.population[10].clear(0.2)
    algorithm.population[10].run_game()


if __name__ == '__main__':
    main()
