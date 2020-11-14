from snake import Snake
from board import Board
from food import Food


class Game_logic:
    def __init__(self):
        '''
        Cała logika gry!
        Ważne jest zliczanie punktów oraz liczby wykonanych przez węża ruchów
        '''
        self.points = 0
        self.move_count = 0
        self.board = Board()
        self.snake = Snake(self.board)
        self.apple = Food(self.snake, self.board)
        self.print_game()
        self.snake.move_snake()
        self.snake.extend_snake()
        self.print_game()
        self.snake.move_snake()
        self.print_game()
        self.snake.move_snake()
        self.print_game()

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

        # print('#' * (self.board.xsize+2)) # odkomenotwać kiedyś

        # To tylko do ogarniania numerów kolumn
        # później odkomentować to na górze
        print('#', end='')
        for i in range(self.board.xsize):
            print(i % 10, end='')
        print('#')
