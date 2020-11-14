from random import randint
from snake import Snake
from board import Board


class Food:
    def __init__(self, snake: Snake, board: Board):
        '''
        Położenie jedzonka jest losowane z dostępnej przestrzeni
        Czyli trzeba uwzględnić miejsce zajęte przez węża
        '''
        # przypisanie węża i planszy żeby ogarniać dostępną przestrzeń
        self.snake = snake
        self.board = board
        self.xpos = self.board.xsize // 2
        self.ypos = self.board.ysize // 2 + 4

    def randomize_position(self):
        '''
        Po zjedzeniu jedzonka przez węża trzeba wylosować nowe 
        położenie jedzonka
        '''
        xpos, ypos = randint(0, self.board.xsize-1), randint(0, self.board.ysize-1)
        while((xpos, ypos) in self.snake.position):
            xpos, ypos = randint(0, self.board.xsize-1), randint(0, self.board.ysize-1)

        self.xpos = xpos
        self.ypos = ypos
