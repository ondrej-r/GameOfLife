import numpy as np
import pytest

from config import Config
from game import Game


@pytest.fixture
def patterns_mockup(tmp_path):
    pattern_file = tmp_path / "patterns.json"
    pattern_file.write_text('{"glider": '
                            '[[0, 1], [1, 2], [2, 0], [2, 1], [2, 2]]}')
    return tmp_path


def test_config_defaults(monkeypatch, patterns_mockup):
    monkeypatch.chdir(patterns_mockup)
    config = Config(test_args=[])

    assert config.terminal is True
    assert config.graphical is False
    assert config.width >= 10
    assert config.height >= 10
    assert config.speed == 0.25
    assert config.steps is None
    assert config.rotate is None
    assert isinstance(config.patterns, dict)
    assert "glider" in config.patterns
    assert "random" in config.patterns


def test_config_parse_args(monkeypatch, patterns_mockup):
    monkeypatch.chdir(patterns_mockup)
    args = ["--graphical", "-x", "50", "-y", "40", "-s", "2", "-n", "10", "-r",
            "90", "-p", "glider"]
    config = Config(test_args=args)

    assert config.graphical is True
    assert config.terminal is False
    assert config.width == 50
    assert config.height == 40
    assert pytest.approx(config.speed, 0.001) == 0.5
    assert config.steps == 10
    assert config.rotate == 90
    assert config.pattern == "glider"


def test_game_random_position(patterns_mockup, monkeypatch):
    monkeypatch.chdir(patterns_mockup)
    config = Config(test_args=[])
    game = Game(**config.dictionarize())

    live_cells = np.count_nonzero(game.grid)
    assert live_cells > 0
    assert live_cells <= (game.width * game.height)


def test_game_apply_pattern(patterns_mockup, monkeypatch):
    monkeypatch.chdir(patterns_mockup)
    config = Config(test_args=["-p", "glider"])
    game = Game(**config.dictionarize())

    assert np.count_nonzero(game.grid) > 0


def test_game_apply_rules_birth(monkeypatch, patterns_mockup):
    monkeypatch.chdir(patterns_mockup)
    config = Config(test_args=[])
    game = Game(**{**config.dictionarize(), "width": 3, "height": 3})
    game.grid = np.zeros((3, 3), dtype=int)
    game.grid[1, 0] = 1
    game.grid[1, 1] = 1
    game.grid[1, 2] = 1

    game.get_neighbors()
    game.apply_rules()

    assert game.grid[0, 1] == 1
    assert game.grid[1, 1] == 1
    assert game.grid[2, 1] == 1


def test_game_apply_rules_death(monkeypatch, patterns_mockup):
    monkeypatch.chdir(patterns_mockup)
    config = Config(test_args=[])
    game = Game(**{**config.dictionarize(), "width": 3, "height": 3})
    game.grid = np.zeros((3, 3), dtype=int)
    game.grid[1, 1] = 1
    game.grid[1, 2] = 1

    game.get_neighbors()
    game.apply_rules()

    assert game.grid[1, 1] == 0


def test_game_rotation(patterns_mockup, monkeypatch):
    monkeypatch.chdir(patterns_mockup)
    config = Config(test_args=["-p", "glider", "-r", "90"])
    game = Game(**config.dictionarize())

    unrotated_config = Config(test_args=["-p", "glider"])
    unrotated_game = Game(**unrotated_config.dictionarize())

    assert not np.array_equal(game.grid, unrotated_game.grid)


def test_game_steps(patterns_mockup, monkeypatch):
    monkeypatch.chdir(patterns_mockup)
    config = Config(test_args=["-n", "5"])
    game = Game(**config.dictionarize())

    for _ in range(config.steps):
        game.get_neighbors()
        game.apply_rules()

    assert game.grid.shape == (config.height, config.width)
