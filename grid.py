from boid import *
import numpy as np


class Grid:
    def __init__(self, cell_width, cell_height, total_width, total_height):
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.total_width = total_width
        self.total_height = total_height

        self.rows = int(np.ceil(total_width / cell_width))
        self.cols = int(np.ceil(total_height / cell_height))

        self.real_width = self.rows * cell_width
        self.real_height = self.cols * cell_height

        self.width_off = (total_width - self.real_width) / 2
        self.height_off = (total_height - self.real_height) / 2

    def create_cells(self):
        cell_cords = [[[] for _ in range(self.cols)] for _ in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.cols):
                cell_cords[i][j] = [(self.cell_width * j) + self.width_off, (self.cell_height * i) + self.height_off]

        return cell_cords


a = Grid(30, 20, 100, 100)
apple = a.create_cells()
for i in apple:
    print(i)
