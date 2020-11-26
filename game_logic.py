from snake import *
from board import Board
from food import Food
from time import sleep
from math import atan2, pi
from neural_net import *


class Game_logic:
    def __init__(self, print_timeout=False):
        '''
        Cała logika gry!
        Ważne jest zliczanie punktów oraz liczby wykonanych przez węża ruchów
        '''
        self.game_over = False
        self.print_timeout = print_timeout  # co ile odświeżać obraz - czas w sekundach
        self.points = 0
        self.move_count = 0
        self.board = Board()
        self.snake = Snake(self.board)
        self.apple = Food(self.snake, self.board)
        self.neural_network = NeuralNetwork()
        self.last_food_move_number = 0  # na jakiej liczbie był licznik ruchów, gdy wąż ostatnio jadł

    def clear(self, print_timeout=False):
        '''
        Przywrócenie game_logic do wartości podstawowych
        '''
        self.game_over = False
        self.points = 0
        self.move_count = 0
        self.snake = Snake(self.board)
        self.apple = Food(self.snake, self.board)
        self.last_food_move_number = 0  # na jakiej liczbie był licznik ruchów, gdy wąż ostatnio jadł
        self.print_timeout = print_timeout  # co ile odświeżać obraz - czas w sekundach

    def print_game(self):
        '''
        Narysowanie gry na ekraniku
        # - ściana
        @ - ciało węża
        O - głowa węża
        $ - jedzonko
        '''
        print(f'Points: {self.points}')
        print(f'Moves: {self.move_count}')
        print('#' * (self.board.xsize+2))
        for row in range(self.board.ysize):
            print('#', end='')
            for col in range(self.board.xsize):
                if (col, row) in self.snake.position:
                    if self.snake.position.index((col, row)) == 0:
                        print('O', end='')
                    else:
                        print('@', end='')
                elif col == self.apple.xpos and row == self.apple.ypos:
                    print('$', end='')
                else:
                    print(' ', end='')
            print('#')
        print('#' * (self.board.xsize+2))

    def check_collisions(self):
        '''
        Koniec gry gdy wąż uderzy w ścianę lub swój ogon
        '''
        head_xpos, head_ypos = self.snake.position[0]
        if head_xpos == -1 or head_xpos == self.board.xsize \
                or head_ypos == -1 or head_ypos == self.board.ysize \
                or (head_xpos, head_ypos) in self.snake.position[1:]:
            self.game_over = True

    def check_food(self):
        '''
        Sprawdzenie czy wąż zjadł jedzonko
        Jeśli tak, to zwiększ punkty, wylosuj nowe jedzonko i wydłuż węża
        '''
        if (self.apple.xpos, self.apple.ypos) in self.snake.position:
            self.points += 1
            self.apple.randomize_position()
            self.snake.extend_snake()
            self.last_food_move_number = self.move_count

    def check_starve(self, C=100):
        if self.move_count-self.last_food_move_number > C:
            self.game_over = True

    def move_snake(self):
        '''
        Poruszenie węża o jedno pole
        '''
        self.move_count += 1
        self.snake.move_snake()

    def distance_left_obstacle(self):
        '''
        Wyznaczenie odległość od przeszkody z 
        lewej strony względem węża. 
        Zwraca wartość znormalizowaną!!!
        '''
        head_xpos, head_ypos = self.snake.position[0]
        normalize = max(self.board.xsize, self.board.ysize)

        if self.snake.move_direction == Direction.UP:
            dist = [head_xpos-x for x, y in self.snake.position[1:] if x < head_xpos and y == head_ypos]
            dist.append(head_xpos)
            return min(dist) / normalize

        elif self.snake.move_direction == Direction.DOWN:
            dist = [x-head_xpos for x, y in self.snake.position[1:] if x > head_xpos and y == head_ypos]
            dist.append(self.board.xsize - head_xpos)
            return min(dist) / normalize

        elif self.snake.move_direction == Direction.RIGHT:
            dist = [head_ypos-y for x, y in self.snake.position[1:] if y < head_ypos and x == head_xpos]
            dist.append(head_ypos)
            return min(dist) / normalize

        else:
            dist = [y-head_ypos for x, y in self.snake.position[1:] if y > head_ypos and x == head_xpos]
            dist.append(self.board.ysize - head_ypos)
            return min(dist) / normalize

    def distance_right_obstacle(self):
        '''
        Wyznaczenie odległość od przeszkody z 
        prawej strony względem węża.
        Zwraca wartość znormalizowaną!!!
        '''
        head_xpos, head_ypos = self.snake.position[0]
        normalize = max(self.board.xsize, self.board.ysize)

        if self.snake.move_direction == Direction.UP:
            dist = [x-head_xpos for x, y in self.snake.position[1:] if x > head_xpos and y == head_ypos]
            dist.append(self.board.xsize - head_xpos)
            return min(dist) / normalize

        elif self.snake.move_direction == Direction.DOWN:
            dist = [head_xpos-x for x, y in self.snake.position[1:] if x < head_xpos and y == head_ypos]
            dist.append(head_xpos)
            return min(dist) / normalize

        elif self.snake.move_direction == Direction.RIGHT:
            dist = [y-head_ypos for x, y in self.snake.position[1:] if y > head_ypos and x == head_xpos]
            dist.append(self.board.ysize - head_ypos)
            return min(dist) / normalize

        else:
            dist = [head_ypos-y for x, y in self.snake.position[1:] if y < head_ypos and x == head_xpos]
            dist.append(head_ypos)
            return min(dist) / normalize

    def distance_front_obstacle(self):
        '''
        Wyznaczenie odległość od przeszkody
        znajdującej się przed wężem.
        Zwraca wartość znormalizowaną!!!
        '''
        head_xpos, head_ypos = self.snake.position[0]
        normalize = max(self.board.xsize, self.board.ysize)

        if self.snake.move_direction == Direction.UP:
            dist = [head_ypos-y for x, y in self.snake.position[1:] if y < head_ypos and x == head_xpos]
            dist.append(head_ypos)
            return min(dist) / normalize

        elif self.snake.move_direction == Direction.DOWN:
            dist = [y-head_ypos for x, y in self.snake.position[1:] if y > head_ypos and x == head_xpos]
            dist.append(self.board.ysize - head_ypos)
            return min(dist) / normalize

        elif self.snake.move_direction == Direction.RIGHT:
            dist = [x-head_xpos for x, y in self.snake.position[1:] if x > head_xpos and y == head_ypos]
            dist.append(self.board.xsize - head_xpos)
            return min(dist) / normalize

        else:
            dist = [head_xpos-x for x, y in self.snake.position[1:] if x < head_xpos and y == head_ypos]
            dist.append(head_xpos)
            return min(dist) / normalize

    def calc_food_snake_angle(self):
        '''
        Wyznaczenie kąta pomiędzy wężem a jabłkiem
        względem węża
        '''
        head_xpos, head_ypos = self.snake.position[0]

        if self.snake.move_direction == Direction.UP:
            x = self.apple.xpos - head_xpos
            y = head_ypos - self.apple.ypos

        elif self.snake.move_direction == Direction.DOWN:
            x = head_xpos - self.apple.xpos
            y = self.apple.ypos - head_ypos

        elif self.snake.move_direction == Direction.RIGHT:
            y = self.apple.xpos - head_xpos
            x = self.apple.ypos - head_ypos

        else:
            y = head_xpos - self.apple.xpos
            x = head_ypos - self.apple.ypos

        return atan2(y, x)

    def set_snake_direction(self, direction):
        '''
        Zmiana kierunku poruszania się węża
        '''
        self.snake.set_direction(direction)

    def generate_direction(self):
        '''
        Odpytywanie sieci neuronowej w celu wyznaczenia
        kierunku poruszania się wężyka.
        Funkcja powinna zwracać 0, 1 lub 2.
        '''
        input = [self.distance_left_obstacle(), self.distance_right_obstacle(), self.distance_front_obstacle(), self.calc_food_snake_angle()]
        return np.argmax(self.neural_network(input), axis=-1)

    def run_game(self):
        '''
        Funkcja zawierająca pętlę wykonania gry
        '''
        while not self.game_over:
            if self.print_timeout:
                self.print_game()
                sleep(self.print_timeout)

            direction = self.generate_direction()
            self.set_snake_direction(direction)
            self.move_snake()
            self.check_food()
            self.check_collisions()
            self.check_starve()

        return self.points, self.move_count
