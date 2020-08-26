# Sudoku-Solver
Sudoku Solver using the Backtracking algorithm and pygame for visualizations.

# About Pygame
Pygame is a python library used for creating 2D and 3D games and applications. This program uses pygame as well, so before running it one must install pygame first. For more information on how to do that based on your platform please visit the [Getting Started](https://www.pygame.org/wiki/GettingStarted) pygame page. I have developed this application with pygame2 in mind and using version 2's documentation so it is preferable for one to use version 2 of the librray.

# Usage
Python version 3 is the recommended version to use when running this. File main.py provides a shebang, which defaults to the latest version of python 3 so one can simply run main.py in terminal like an executable:
```
./main.py [options]
```
For more detailed information regarding the options, type:
```
./main.py --help
```

# Examples
### Run a normal speed solver with the easy board
```
./main.py -p ./boards/game1.json
```

### Run a fast solver with the expert board
```
./main.py -p ./boards/expert_game.json --fast
```

To restart the board press TAB.
To exit press either ESCAPE or the corresponding key combination to close apps on your OS. For example on macOS - ⌘+Q

# Supplying one's own boards
One can also supply their own board and run the solver on it. To do it one needs to supply a json file in the following format:
```json
{
    "board" {
        "row1": [number1,number2,number3,number4,number5,number6,number7,number8,number9],
        "row2": [number1,number2,number3,number4,number5,number6,number7,number8,number9],
        ...
        "row9": [number1,number2,number3,number4,number5,number6,number7,number8,number9]
    }
}
```
There's a global "board" key, which contains keys named "row[1-9]" each representing a list of all 9 numbers in the given row.