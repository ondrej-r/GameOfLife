from game_of_life import Config

def test_argument_parsing():
    test_args = ["-t", "-x", "40", "-y", "30", "-s", "0.5", "-n", "10", "-p", "glider"]

    config = Config(test_args)
    
    assert config.args.terminal == True
    assert config.args.graphical == False
    assert config.args.width == 40
    assert config.args.height == 30
    assert config.args.speed == 0.5
    assert config.args.steps == 10
    assert config.args.pattern == "glider"

# Add more specific test cases for each argument as needed


"""
import numpy as np
import json
from game_of_life import Config, Game

def test_apply_pattern_spaceship():
    test_args = ["-t", "-x", "40", "-y", "30", "-s", "0.5", "-n", "10", "-p", "glider"]
    config = Config(test_args)
    game = Game(**config.dictionarize())
    with open("patterns.json", "r") as f:
        patterns = dict(json.load(f))
        assert len(patterns["spaceship"]) == 9

def test_random_position():
    test_args = ["-t", "-x", "40", "-y", "30", "-s", "0.5", "-n", "10", "-p", "glider"]
    config = Config(test_args)
    game = Game(**config.dictionarize())
    game.random_position()
    assert 0 <= np.count_nonzero(game.grid) <= (game.width // 3) * (game.height // 3)

def test_get_neighbors():
    test_args = ["-t", "-x", "40", "-y", "30", "-s", "0.5", "-n", "10", "-p", "glider"]
    config = Config(test_args)
    game = Game(**config.dictionarize())
    game.get_neighbors()
    assert game.neighbors.shape == game.grid.shape

def test_apply_rules():
    test_args = ["-t", "-x", "40", "-y", "30", "-s", "0.5", "-n", "10", "-p", "glider"]
    config = Config(test_args)
    game = Game(**config.dictionarize())
    game.get_neighbors()
    game.apply_rules()
    assert game.grid.shape == game.neighbors.shape

def test_argument_parsing():
    test_args = ["-t", "-x", "40", "-y", "30", "-s", "0.5", "-n", "10", "-p", "glider"]
    config = Config(test_args)
    game = Game(**config.dictionarize())

    assert game.config.terminal
    assert not game.config.graphical
    assert game.config.width == 40
    assert game.config.height == 30
    assert game.config.speed == 0.5
    assert game.config.steps == 10
    assert game.config.pattern == "glider"
"""