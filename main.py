from genetic_algorithm import *


def main():
    algorithm = GeneticAlgorithm(max_generation=20, population_size=32)
    best_snake = algorithm.get_best_snake(0.2)
    best_snake.run_game()


if __name__ == '__main__':
    main()
