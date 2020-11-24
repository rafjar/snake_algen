from snake import *
from board import Board
from food import Food
from time import sleep
from math import atan2, pi


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
        self.run_game()

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

    def move_snake(self):
        '''
        Poruszenie węża o jedno pole
        '''
        self.move_count += 1
        self.snake.move_snake()

    def calc_food_snake_angle(self):
        '''
        Wyznaczenie kąta pomiędzy wężem a jabłkiem
        względem węża
        '''
        head_xpos, head_ypos = self.snake.position[0]

        if self.snake.move_direction == Direction.UP:
            x = self.apple.xpos - head_xpos
            y = head_ypos - self.apple.ypos
            return atan2(y, x)
        elif self.snake.move_direction == Direction.DOWN:
            x = head_xpos - self.apple.xpos
            y = self.apple.ypos - head_ypos
            return atan2(y, x)
        elif self.snake.move_direction == Direction.RIGHT:
            y = self.apple.xpos - head_xpos
            x = self.apple.ypos - head_ypos
            return atan2(y, x)
        elif self.snake.move_direction == Direction.LEFT:
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
        pass

    def run_game(self):
        '''
        Funkcja zawierająca pętlę wykonania gry
        '''
        while not self.game_over:
            if self.print_timeout:
                self.print_game()
                sleep(self.print_timeout)

            self.calc_food_snake_angle()
            self.set_snake_direction(self.generate_direction())
            self.move_snake()
            self.check_food()
            self.check_collisions()
