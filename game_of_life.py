import os
import argparse
import sys
import json
import numpy as np
from time import sleep
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = ""
import pygame  # noqa: E402 ignore due to setting enviroment variable


class Config:
    def __init__(self, test_args=None):
        """
        Initializes Config class.

        Parameters:
            test_args (list, optional):
                List of arguments to use with library pytest. Default is None.
        """
        self.patterns = self._load_patterns()
        self.args = self._parse_args(test_args)
        self._init_values()

    def _parse_args(self, args=None):
        """
        Parses command line arguments.

        Parameters:
            args (list, optional):
                Adds list of availible arguments. Default is None.
        Returns:
            Namespace: Parsed arguments namespace.
        """
        parser = argparse.ArgumentParser(description="Conway's Game of Life")
        parser.add_argument("-t", "--terminal", "--tui", action="store_true")
        parser.add_argument("-g", "--graphical", "--gui", action="store_true")
        parser.add_argument("-x", "--width", type=int, help="")
        parser.add_argument("-y", "--height", type=int, help="")
        parser.add_argument("-s", "--speed", type=float, help="")
        parser.add_argument("-n", "--steps", type=int, help="")
        parser.add_argument("-r", "--rotate", type=int, help="")
        parser.add_argument("-p", "--pattern",
                            choices=self.patterns.keys(),
                            nargs="?",  # make it optional
                            help="use a pattern for the Game of Life")
        parsed_args = parser.parse_args(args)

        if parsed_args.pattern is None and "-p" in sys.argv:
            print("Showing available patterns:")
            print(", ".join(self.patterns.keys()))
            sys.exit(0)

        return parsed_args

    def _init_values(self):
        """
        Initializes configuration values from parsed arguments or defaults.
        """
        try:
            term_width, term_height = os.get_terminal_size()
        except OSError:
            term_width, term_height = 80, 24
        term_width //= 2

        self.terminal = (
            self.args.terminal or not self.args.graphical
        )
        self.graphical = (
            self.args.graphical and not self.args.terminal
        )
        self.width = max(
            10,
            self.args.width if self.args.width else term_width
        )
        self.height = max(
            10,
            self.args.height if self.args.height else term_height
        )
        self.speed = (
            1 / self.args.speed if self.args.speed and self.args.speed > 0
            else 0.25
        )
        self.steps = (
            self.args.steps if self.args.steps and self.args.steps > 0
            else None
        )
        self.rotate = (
            round(self.args.rotate / 90) * 90 % 360
            if self.args.rotate else None
        )
        self.pattern = (
            self.args.pattern.lower()
            if self.args.pattern else None
        )

    def _load_patterns(self):
        """
        Loads predefined patterns from patterns.json.

        Returns:
            dict: Dictionary of pattern names and respective lists of cells.
        """
        try:
            with open("patterns.json", "r") as f:
                patterns = dict(json.load(f))
                patterns["random"] = []
                return patterns
        except FileNotFoundError:
            return {"random": []}

    def dictionarize(self):
        """
        Converts configuration parameters into a dictionary.

        Returns:
            dict: Dictionary of config attributes and values.
        """
        return {
            "terminal": self.terminal,
            "graphical": self.graphical,
            "width": self.width,
            "height": self.height,
            "speed": self.speed,
            "steps": self.steps,
            "rotate": self.rotate,
            "patterns": self.patterns,
            "pattern": self.pattern,
        }


class Game:
    def __init__(self, **config):
        """
        Initializes Game class and grid.

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
        Applies selected starting pattern to the grid.
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
        Applies simulation rules to all cells and updates the grid to the next
        step.
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
        Prints the current grid state as text to the console.
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
        Performs one step of text user interface simulation.
        """
        self.print_tui()
        self.get_neighbors()
        self.apply_rules()

    def run_tui(self):
        """
        Runs the simulation in the console.
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
        Setups graphical user interface using PyGame.
        """
        self.cell_size = 20
        pygame.init()
        self.screen = pygame.display.set_mode(
            (self.width * self.cell_size, self.height * self.cell_size))
        self.clock = pygame.time.Clock()

    def draw_gui(self):
        """
        Draws the current state of the grid in a window.
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
        Performs one step of graphical user interface simulation.
        """
        self.get_neighbors()
        self.apply_rules()
        self.draw_gui()

    def run_gui(self):
        """
        Runs the simulation in a graphical PyGame window.
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
        Switches between text and graphical version of the simulation.
        """
        if self.graphical:
            self.run_gui()
        else:
            self.run_tui()


if __name__ == "__main__":
    config = Config()
    game = Game(**config.dictionarize())
    game.main()
