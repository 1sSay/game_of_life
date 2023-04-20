import random
import time

import cv2 as cv
import numpy as np


class GameOfLife:
    def __init__(
        self, field_size: tuple, cells: list, resize_coefficient: int = 1
    ) -> None:
        self.field = None
        self.alive_cells = list()
        self.resize_coefficient = resize_coefficient
        self.greed = 0

        self.create_field(field_size)
        self.set_start_position(cells)

    def create_field(self, size: tuple) -> None:
        self.field = np.zeros(size, dtype=np.uint8)

    def set_start_position(self, cells: list) -> None:
        self.alive_cells = cells
        self.field = np.zeros(self.field.shape, dtype=np.uint8)

    def clear(self):
        self.create_field(self.field.shape)
        self.set_start_position(list())

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

    def prepare_frame(self) -> np.array:
        img = cv.resize(
            self.field,
            [i * self.resize_coefficient for i in self.field.shape],
            interpolation=cv.INTER_NEAREST,
        )
        
        if self.greed:
            for i in range(1, self.field.shape[0]):
                img[i * self.resize_coefficient, :] = 64
            for j in range(1, self.field.shape[1]):
                img[:, j * self.resize_coefficient] = 64

        return img

    def play(self, iterations: int) -> np.array:
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

            yield self.prepare_frame()


def mouse_event(event, x, y, flags, param):
    x = x // RESIZE_COEFFICIENT
    y = y // RESIZE_COEFFICIENT

    if event == cv.EVENT_LBUTTONDOWN:
        cell_status = game.field[y, x]

        if cell_status == 0:
            game.field[y, x] = 255
            game.alive_cells.append((y, x))
        else:
            game.field[y, x] = 0
            game.alive_cells.remove((y, x))

        cv.imshow("Game of Life", game.prepare_frame())


if __name__ == "__main__":
    FIELD_SIZE = (100, 100)
    ITERATIONS = 10000
    RESIZE_COEFFICIENT = 8
    RANDOM_CELLS_COUNT = 0

    cv.namedWindow("Game of Life")
    cv.setMouseCallback("Game of Life", mouse_event)

    start_cells = list()
    for i in range(RANDOM_CELLS_COUNT):
        start_cells.append(
            (random.randint(0, FIELD_SIZE[0] - 1), random.randint(0, FIELD_SIZE[1] - 1))
        )

    game = GameOfLife(FIELD_SIZE, start_cells, resize_coefficient=RESIZE_COEFFICIENT)

    for frame in game.play(ITERATIONS):
        cv.imshow("Game of Life", frame)
        
        if (cv.waitKey(100) & 0xFF) == ord("q"):
            while True:
                event = cv.waitKey(100) & 0xFF
                if event == ord("q"):
                    break
                if event == ord("d"):
                    game.clear()
                    cv.imshow("Game of Life", game.prepare_frame())
                if event == ord("g"):
                    game.greed = (not game.greed)
                    cv.imshow("Game of Life", game.prepare_frame())