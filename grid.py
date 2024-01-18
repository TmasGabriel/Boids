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
        self.boid_storage = [[[] for _ in range(self.cols)] for _ in range(self.rows)]

    def create_grid(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.cell_cords[i][j] = [int((self.cell_width * j) + self.width_off),
                                    int((self.cell_height * i) + self.height_off)]
        return self.cell_cords

    def in_cell(self, boid):
        self.boid_storage[int(boid.center[0] // self.cell_width)][int(boid.center[1] // self.cell_height)].append(boid)
        return self.boid_storage

    def adj_cells(self, cell):
        adjacent_cells = []
        for row_offset in range(-1, 2):
            for col_offset in range(-1, 2):
                if row_offset == 0 and col_offset == 0:
                    continue  # Skip the original cell itself
                new_row, new_col = cell[0] + row_offset, cell[1] + col_offset
                if 0 <= new_row < self.rows and 0 <= new_col < self.cols:
                    adjacent_cells.append([new_row, new_col])

        return adjacent_cells
