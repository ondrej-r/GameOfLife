import os
import sys
from time import sleep

import numpy as np

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = ""
import pygame  # noqa: E402 ignore due to setting enviroment variable


class Game:
    def __init__(self, **config):
        """
        Initializes the Game class with configuration parameters and sets up the game grid.
        
        Parameters:
            **config:
                Keyword arguments unpacked from a configuration dictionary.
        """
        self.__dict__.update(config)
        self.grid = np.zeros((self.height, self.width), dtype=int)
        if self.pattern in self.patterns.keys() and self.pattern != "random":
            self.apply_pattern()
        else:
            self.random_position()

    def apply_pattern(self):
        """
        Applies the selected pattern to the grid, accounting for rotation.
        """
        cells = self.patterns[self.pattern]
        if self.rotate == 90:
            cells = [(-y, x) for x, y in cells]
        elif self.rotate == 180:
            cells = [(-x, -y) for x, y in cells]
        elif self.rotate == 270:
            cells = [(y, -x) for x, y in cells]
        center_x = (max(x for x, y in cells) + min(x for x, y in cells)) // 2
        offset_x = (self.width // 2) - center_x

        center_y = (max(y for x, y in cells) + min(y for x, y in cells)) // 2
        offset_y = (self.height // 2) - center_y
        for x, y in cells:
            grid_x = x + offset_x
            grid_y = y + offset_y
            if 0 <= grid_x < self.width and 0 <= grid_y < self.height:
                self.grid[grid_y, grid_x] = 1

    def random_position(self):
        """
        Fills section of the grid with randomly placed live cells.
        """
        for x in range(self.width // 3, 2 * self.width // 3):
            for y in range(self.height // 3, 2 * self.height // 3):
                self.grid[y, x] = np.random.randint(0, 2)

    def get_neighbors(self):
        """
        Computes and stores count of live neighbors for every cell in the grid.
        """
        self.neighbors = np.zeros_like(self.grid)
        for row in range(self.height):
            for col in range(self.width):
                count = 0
                for x in range(-1, 2):
                    for y in range(-1, 2):
                        if x == 0 and y == 0:
                            continue  # skip cell
                        neighbor_row = (row + x) % self.height
                        neighbor_col = (col + y) % self.width
                        count += self.grid[neighbor_row, neighbor_col]
                self.neighbors[row, col] = count

    def apply_rules(self):
        """
        Applies simulation rules to all cells and updates the grid accordingly.
        """
        new_grid = np.zeros_like(self.grid)
        for row in range(self.height):
            for col in range(self.width):
                if self.grid[row, col] == 1:  # cell is alive
                    if self.neighbors[row, col] not in [2, 3]:  # cell dies
                        new_grid[row, col] = 0
                    else:  # cell survives
                        new_grid[row, col] = 1
                else:
                    if self.neighbors[row, col] == 3:  # cell is born
                        new_grid[row, col] = 1
        self.grid = new_grid  # update grid

    def print_tui(self):
        """
        Prints the current grid state in the terminal.
        """
        for row in range(self.height):
            for col in range(self.width):
                if (self.grid[row, col] == 1):
                    print("██", end="")
                else:
                    print("  ", end="")
            if not self.width % 2:
                print(" ", end="")
            print()
        print(flush=True, end="")

    def step_tui(self):
        """
        Performs one step of simulation in the terminal.
        """
        self.print_tui()
        self.get_neighbors()
        self.apply_rules()

    def run_tui(self):
        """
        Runs the simulation in the terminal.
        """
        if self.steps is not None:
            for _ in range(self.steps):
                self.step_tui()
                sleep(self.speed)
        else:
            while True:
                self.step_tui()
                sleep(self.speed)

    def setup_gui(self):
        """
        Sets up the graphical user interface using PyGame.
        """
        self.cell_size = 20
        pygame.init()
        self.screen = pygame.display.set_mode(
            (self.width * self.cell_size, self.height * self.cell_size))
        self.clock = pygame.time.Clock()

    def draw_gui(self):
        """
        Draws the current state of the grid to the graphical window.
        """
        self.screen.fill((0, 0, 0))
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x]:
                    pygame.draw.rect(
                        self.screen, (255, 255, 255),
                        (x * self.cell_size, y * self.cell_size,
                         self.cell_size, self.cell_size)
                    )
        pygame.display.flip()

    def step_gui(self):
        """
        Performs one step of simulation in the graphical window.
        """
        self.get_neighbors()
        self.apply_rules()
        self.draw_gui()

    def run_gui(self):
        """
        Runs the simulation in the graphical window.
        """
        self.setup_gui()
        step_counter = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
            if self.steps is None or step_counter < self.steps:
                self.step_gui()
                step_counter += 1
            else:
                self.draw_gui()
            self.clock.tick(1 / self.speed)

    def main(self):
        """
        Main entry point for the simulation.
        Switches between text and graphical version of the simulation.
        """
        if self.graphical:
            self.run_gui()
        else:
            self.run_tui()
