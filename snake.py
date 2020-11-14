from board import Board
from enum import Enum

import copy

# Enum zawierający kierunki wężowe
Direction = Enum('Direction', 'UP DOWN LEFT RIGHT')


class Snake:
    def __init__(self, board: Board):
        '''
        Położenie początkowe głowy węża to środek planszy
        Reszta ciała węża ułożona w górę
        Początkowo wąż porusza się w dół
        Głową węża to position[0] - położenia podawane są w formacie (x, y)
        '''
        xpos, ypos = board.xsize//2, board.ysize//2
        self.position = [(xpos, ypos), (xpos, ypos-1), (xpos, ypos-2)]
        self.move_direction = Direction.DOWN

    def set_direction(self, new_pos):
        '''
        Zmiana kierunku poruszania się węża
        new_pos to jedna z trzech liczb: 0, 1, 2
        0 - skręć w lewo
        1 - idź prosto
        2 - skręć w prawo
        '''
        if self.move_direction == Direction.UP:
            if new_pos == 0:
                self.move_direction = Direction.LEFT
            elif new_pos == 2:
                self.move_direction = Direction.RIGHT

        elif self.move_direction == Direction.RIGHT:
            if new_pos == 0:
                self.move_direction = Direction.UP
            elif new_pos == 2:
                self.move_direction = Direction.DOWN

        elif self.move_direction == Direction.DOWN:
            if new_pos == 0:
                self.move_direction = Direction.RIGHT
            elif new_pos == 2:
                self.move_direction = Direction.LEFT

        elif self.move_direction == Direction.LEFT:
            if new_pos == 0:
                self.move_direction = Direction.DOWN
            elif new_pos == 2:
                self.move_direction = Direction.UP

    def move_snake(self):
        '''
        Poruszenie węża zgodnie z kierunkiem self.move_direction
        '''
        old_pos = copy.copy(self.position)
        head_xpos, head_ypos = self.position[0]

        if self.move_direction == Direction.UP:
            self.position[0] = (head_xpos, head_ypos-1)
        elif self.move_direction == Direction.RIGHT:
            self.position[0] = (head_xpos+1, head_ypos)
        elif self.move_direction == Direction.DOWN:
            self.position[0] = (head_xpos, head_ypos+1)
        else:
            self.position[0] = (head_xpos-1, head_ypos)

        for i in range(1, len(self.position)):
            self.position[i] = old_pos[i-1]

    def extend_snake(self):
        '''
        Jak wąż zje jedzonko, to trzeba go wydłużyć
        '''
        pass
