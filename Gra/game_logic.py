from snake import *
from board import Board
from food import Food
from time import sleep
from math import atan2, pi


class Game_logic:
    def __init__(self):
        '''
        Cała logika gry!
        Ważne jest zliczanie punktów oraz liczby wykonanych przez węża ruchów
        '''
        self.game_over = False
        self.points = 0
        self.move_count = 0
        self.board = Board()
        self.snake = Snake(self.board)
        self.apple = Food(self.snake, self.board)
        self.last_food_move_number = 0  # na jakiej liczbie był licznik ruchów, gdy wąż ostatnio jadł

    def clear(self):
        '''
        Przywrócenie game_logic do wartości podstawowych
        '''
        self.game_over = False
        self.points = 0
        self.move_count = 0
        self.snake = Snake(self.board)
        self.apple = Food(self.snake, self.board)
        self.last_food_move_number = 0  # na jakiej liczbie był licznik ruchów, gdy wąż ostatnio jadł

    def print_game(self):
        '''
        Narysowanie gry na ekraniku
        # - ściana
        @ - ciało węża
        O - głowa węża
        $ - jedzonko
        '''
        head_xpos, head_ypos = self.snake.position[0]
        obstacle_left, obstacle_front, obstacle_right = None, None, None

        if self.snake.move_direction == Direction.DOWN:
            for distance in range(1, self.board.xsize+1):
                xminus, xplus = head_xpos-distance, head_xpos+distance
                if obstacle_left is None and (xminus == -1 or (xminus, head_ypos) in self.snake.position[1:]):
                    obstacle_left = (xminus, head_ypos)
                if obstacle_right is None and (xplus == self.board.xsize or (xplus, head_ypos) in self.snake.position[1:]):
                    obstacle_right = (xplus, head_ypos)
            for distance in range(1, self.board.ysize+1):
                yplus = head_ypos+distance
                if obstacle_front is None and (yplus == self.board.ysize or (head_xpos, yplus) in self.snake.position[1:]):
                    obstacle_front = (head_xpos, yplus)

        elif self.snake.move_direction == Direction.UP:
            for distance in range(1, self.board.xsize+1):
                xminus, xplus = head_xpos-distance, head_xpos+distance
                if obstacle_right is None and (xplus == self.board.xsize or (xplus, head_ypos) in self.snake.position[1:]):
                    obstacle_right = (xplus, head_ypos)
                if obstacle_left is None and (xminus == -1 or (xminus, head_ypos) in self.snake.position[1:]):
                    obstacle_left = (xminus, head_ypos)
            for distance in range(1, self.board.ysize+1):
                yminus = head_ypos-distance
                if obstacle_front is None and (yminus == -1 or (head_xpos, yminus) in self.snake.position[1:]):
                    obstacle_front = (head_xpos, yminus)

        elif self.snake.move_direction == Direction.LEFT:
            for distance in range(1, self.board.ysize+1):
                yminus, yplus = head_ypos-distance, head_ypos+distance
                if obstacle_left is None and (yplus == self.board.ysize or (head_xpos, yplus) in self.snake.position[1:]):
                    obstacle_left = (head_xpos, yplus)
                if obstacle_right is None and (yminus == -1 or (head_xpos, yminus) in self.snake.position[1:]):
                    obstacle_right = (head_xpos, yminus)
            for distance in range(1, self.board.xsize+1):
                xminus = head_xpos-distance
                if obstacle_front is None and (xminus == -1 or (xminus, head_ypos) in self.snake.position[1:]):
                    obstacle_front = (xminus, head_ypos)

        elif self.snake.move_direction == Direction.RIGHT:
            for distance in range(1, self.board.ysize+1):
                yminus, yplus = head_ypos-distance, head_ypos+distance
                if obstacle_right is None and (yplus == self.board.ysize or (head_xpos, yplus) in self.snake.position[1:]):
                    obstacle_right = (head_xpos, yplus)
                if obstacle_left is None and (yminus == -1 or (head_xpos, yminus) in self.snake.position[1:]):
                    obstacle_left = (head_xpos, yminus)
            for distance in range(1, self.board.xsize+1):
                xplus = head_xpos+distance
                if obstacle_front is None and (xplus == self.board.xsize or (xplus, head_ypos) in self.snake.position[1:]):
                    obstacle_front = (xplus, head_ypos)

        obstacles = (obstacle_front, obstacle_left, obstacle_right)
        
        print(f'Points: {self.points}')
        print(f'Moves: {self.move_count}')
        map_str = ''
        for y in range(-1, self.board.ysize+1):
            for x in range(-1, self.board.xsize+1):
                if (x, y) in obstacles:
                    map_str += '#'
                elif (x, y) == (head_xpos, head_ypos):
                    map_str += 'O'
                elif (x, y) == (self.apple.xpos, self.apple.ypos):
                    map_str += '$'
                else:
                    map_str += ' '
            map_str += '\n'
        print(map_str)

    def check_collisions(self):
        '''
        Koniec gry gdy wąż uderzy w ścianę lub swój ogon
        '''
        head_xpos, head_ypos = self.snake.position[0]
        if head_xpos == -1 or head_xpos == self.board.xsize \
                or head_ypos == -1 or head_ypos == self.board.ysize \
                or (head_xpos, head_ypos) in self.snake.position[1:]:
            self.game_over = True
            print('Game over! Snake has crashed.')

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

    def check_starve(self, max_moves_diff=100):
        '''
        Sprawdza czy węż się nie zapętlił. 
        Jeśli wąż nic nie zjadł od ostatnich 'max_moves_diff'
        kroków, to umiera
        '''
        if self.move_count-self.last_food_move_number > max_moves_diff:
            self.game_over = True
            print('Game over! Snake has starved.')

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
        next_direction = input('Choose direction: ')
        if next_direction == 'a':
            return 0
        elif next_direction == 'w':
            return 1
        elif next_direction == 'd':
            return 2
        else:
            print('Incorrect value!\nPress A, W or D to move LEFT, STRAIGHT or RIGHT, respectively.')
            return self.generate_direction()

    def get_points(self):
        return self.points

    def get_move_count(self):
        return self.move_count

    def run_game(self):
        '''
        Funkcja zawierająca pętlę wykonania gry
        '''
        while not self.game_over:
            self.print_game()

            direction = self.generate_direction()
            self.set_snake_direction(direction)
            self.move_snake()
            self.check_food()
            self.check_collisions()
            self.check_starve()

        return self.points, self.move_count
