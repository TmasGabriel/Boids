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

        self.cell_cords = [[[] for _ in range(self.cols)] for _ in range(self.rows)]

    def create_grid(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.cell_cords[i][j] = [int((self.cell_width * j) + self.width_off),
                                    int((self.cell_height * i) + self.height_off)]

        return self.cell_cords

    def in_cell(self, boid):
        return boid[0] // self.cell_width, boid[1] // self.cell_height

    def adj_cells(self, cell):
        adjacent_cells = [[] for _ in range(9)]
        adjacent_cells[0] = cell[0], cell[1]
        adjacent_cells[1] = cell[0] - 1, cell[1] - 1
        adjacent_cells[2] = cell[0] - 1, cell[1]
        adjacent_cells[3] = cell[0] - 1, cell[1] + 1
        adjacent_cells[4] = cell[0],     cell[1] + 1
        adjacent_cells[5] = cell[0] + 1, cell[1] + 1
        adjacent_cells[6] = cell[0] + 1, cell[1]
        adjacent_cells[7] = cell[0] + 1, cell[1] - 1
        adjacent_cells[8] = cell[0],     cell[1] - 1

        return adjacent_cells


a = Grid(20, 30, 100, 100)
a.create_grid()
print()
print(a.adj_cells(a.in_cell([32, 16])))
