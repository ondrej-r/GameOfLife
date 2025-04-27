import argparse
import json
import os
import sys


class Config:
    def __init__(self, test_args=None):
        """
        Initializes the Config class with optional command-line arguments.

        Parameters:
            test_args (list, optional): 
                A list of arguments to be parsed by the library pytest. Default is None.
        """
        self.patterns = self._load_patterns()
        self.args = self._parse_args(test_args)
        self._init_values()

    def _parse_args(self, args=None):
        """
        Parses command-line arguments for the simulation.

        Parameters:
            args (list, optional): 
                A list of arguments to parse.

        Returns:
            Namespace: Parsed arguments namespace containing flags and options.
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
        Initializes configuration values based on parsed arguments or defaults.
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
