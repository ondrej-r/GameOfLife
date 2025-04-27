# Table of Contents

* [config](#config)
  * [Config](#config.Config)
    * [\_\_init\_\_](#config.Config.__init__)
    * [dictionarize](#config.Config.dictionarize)
* [game](#game)
  * [Game](#game.Game)
    * [\_\_init\_\_](#game.Game.__init__)
    * [apply\_pattern](#game.Game.apply_pattern)
    * [random\_position](#game.Game.random_position)
    * [get\_neighbors](#game.Game.get_neighbors)
    * [apply\_rules](#game.Game.apply_rules)
    * [print\_tui](#game.Game.print_tui)
    * [step\_tui](#game.Game.step_tui)
    * [run\_tui](#game.Game.run_tui)
    * [setup\_gui](#game.Game.setup_gui)
    * [draw\_gui](#game.Game.draw_gui)
    * [step\_gui](#game.Game.step_gui)
    * [run\_gui](#game.Game.run_gui)
    * [main](#game.Game.main)

<a id="config"></a>

# config

<a id="config.Config"></a>

## Config Objects

```python
class Config()
```

<a id="config.Config.__init__"></a>

#### \_\_init\_\_

```python
def __init__(test_args=None)
```

Initializes the Config class with optional command-line arguments.

**Arguments**:

  test_args (list, optional):
  A list of arguments to be parsed by the library pytest. Default is None.

<a id="config.Config.dictionarize"></a>

#### dictionarize

```python
def dictionarize()
```

Converts configuration parameters into a dictionary.

**Returns**:

- `dict` - Dictionary of config attributes and values.

<a id="game"></a>

# game

<a id="game.Game"></a>

## Game Objects

```python
class Game()
```

<a id="game.Game.__init__"></a>

#### \_\_init\_\_

```python
def __init__(**config)
```

Initializes the Game class with configuration parameters and sets up the game grid.

**Arguments**:

  **config:
  Keyword arguments unpacked from a configuration dictionary.

<a id="game.Game.apply_pattern"></a>

#### apply\_pattern

```python
def apply_pattern()
```

Applies the selected pattern to the grid, accounting for rotation.

<a id="game.Game.random_position"></a>

#### random\_position

```python
def random_position()
```

Fills section of the grid with randomly placed live cells.

<a id="game.Game.get_neighbors"></a>

#### get\_neighbors

```python
def get_neighbors()
```

Computes and stores count of live neighbors for every cell in the grid.

<a id="game.Game.apply_rules"></a>

#### apply\_rules

```python
def apply_rules()
```

Applies simulation rules to all cells and updates the grid accordingly.

<a id="game.Game.print_tui"></a>

#### print\_tui

```python
def print_tui()
```

Prints the current grid state in the terminal.

<a id="game.Game.step_tui"></a>

#### step\_tui

```python
def step_tui()
```

Performs one step of simulation in the terminal.

<a id="game.Game.run_tui"></a>

#### run\_tui

```python
def run_tui()
```

Runs the simulation in the terminal.

<a id="game.Game.setup_gui"></a>

#### setup\_gui

```python
def setup_gui()
```

Sets up the graphical user interface using PyGame.

<a id="game.Game.draw_gui"></a>

#### draw\_gui

```python
def draw_gui()
```

Draws the current state of the grid to the graphical window.

<a id="game.Game.step_gui"></a>

#### step\_gui

```python
def step_gui()
```

Performs one step of simulation in the graphical window.

<a id="game.Game.run_gui"></a>

#### run\_gui

```python
def run_gui()
```

Runs the simulation in the graphical window.

<a id="game.Game.main"></a>

#### main

```python
def main()
```

Main entry point for the simulation.
Switches between text and graphical version of the simulation.

