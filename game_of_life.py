import random
import time

import cv2 as cv
import numpy as np


class GameOfLife:
    def __init__(self, field_size: tuple, cells: list) -> None:
        self.field = None
        self.alive_cells = list()
        
        self.create_field(field_size)
        self.set_start_position(cells)

    def create_field(self, size: tuple) -> None:
        self.field = np.zeros(size, dtype=np.uint8)

    def set_start_position(self, cells: list) -> None:
        self.alive_cells = cells
        self.field = np.zeros(self.field.shape, dtype=np.uint8)

    def get_around(self, coord: tuple) -> list:
        x, y = coord

        ans = list()
        for i in range(3):
            for j in range(3):
                cur_x = x - 1 + i
                cur_y = y - 1 + j

                if 0 <= cur_x <= 99 and 0 <= cur_y <= 99:
                    ans.append((cur_x, cur_y))

        return ans

    def play(self, iterations: int, resize_coefficient: int=1) -> np.array:
        for it in range(iterations):
            neighbors = dict()

            for alive_cell in self.alive_cells:
                if neighbors.get(alive_cell) is None:
                    neighbors[alive_cell] = 0
                for cell in self.get_around(alive_cell):
                    if cell == alive_cell:
                        continue
                    if neighbors.get(cell) is None:
                        neighbors[cell] = 0
                    neighbors[cell] += 1

            new_alive = list()

            for cell in neighbors:
                x, y = cell
                if neighbors[cell] == 3:
                    new_alive.append(cell)
                    self.field[x][y] = 255
                elif cell in self.alive_cells and neighbors[cell] == 2:
                    new_alive.append(cell)
                elif 2 > neighbors[cell] or neighbors[cell] > 3:
                    self.field[x][y] = 0

            self.alive_cells = new_alive

            img = cv.resize(self.field,
                            [i * resize_coefficient for i in self.field.shape],
                            interpolation=cv.INTER_NEAREST)
            yield img


if __name__ == '__main__':
    FIELD_SIZE = (100, 100)
    ITERATIONS = 1000
    RESIZE_COEFFICIENT = 6
    
    cv.namedWindow('Game of Life')

    start_cells = list()
    for i in range(1000):
        start_cells.append((random.randint(0, FIELD_SIZE[0] - 1),
                            random.randint(0, FIELD_SIZE[1] - 1)))
    
    game = GameOfLife(FIELD_SIZE, start_cells)

    for frame in game.play(ITERATIONS, RESIZE_COEFFICIENT):
        cv.imshow('Game of Life', frame)
        cv.waitKey(5)