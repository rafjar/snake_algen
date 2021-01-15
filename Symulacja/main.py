from genetic_algorithm import *
import matplotlib.pyplot as plt

def main():
    algorithm = GeneticAlgorithm(max_generation=20, population_size=32)
    best_snake = algorithm.get_best_snake(0.2)
    best_snake.run_game()
    
    all_points = algorithm.get_generations_points()
    mean_pts = []
    top_pts = []
    low_pts = []
    for points in all_points:
        top_pts.append(max(points))
        low_pts.append(min(points))
        mean_pts.append(np.mean(points))
    
    plt.figure(figsize=(12, 8))
    plt.plot(top_pts, 'b')
    plt.plot(mean_pts, 'r')
    plt.plot(low_pts, 'c')
    plt.xlabel('Generacja')
    plt.grid()
    plt.legend(('Maksymalna liczba punktów', 'Średnia liczba punktów', 'Minimalna liczba punktów'))
    plt.savefig('wykres.png')
    plt.show()


if __name__ == '__main__':
    main()
