#!/usr/bin/env python3
"""Sudoku Solver using Pygame and the backtracking algorithm
"""

import os
import sys
import enum
import json
import argparse
import pygame
import pygame.freetype


class Color(enum.Enum):
    Background = (38, 49, 50)
    Text = (255, 255, 255)
    CurrentlySolving = (255, 81, 81)
    Solved = (105, 240, 173)
    Grid = (96, 124, 139)


class Cell():
    """Implementation of a single Sudoku cell. Use this class to keep track
    of a cell's color, coordinate positions, and current solution
    """
    def __init__(self, row, col, width, height, number):
        self._row = row
        self._col = col
        self._xpos = col * width
        self._ypos = row * height
        self._color = Color.Background

        if number:
            self._solution = number
        else:
            self._solution = 0

    @property
    def xpos(self):
        return self._xpos

    @xpos.setter
    def xpos(self, new_xpos):
        self._xpos = new_xpos

    @property
    def ypos(self):
        return self._ypos

    @ypos.setter
    def ypos(self, new_ypos):
        self._ypos = new_ypos

    @property
    def solution(self):
        return self._solution

    @solution.setter
    def solution(self, num):
        self._solution = num

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, new_color):
        self._color = new_color

    def __str__(self):
        return str(self._solution) if self._solution else ""


class SudokuGame():
    """Class that implements the logic of solving Sudoku by using
    the Backtracking algorithm
    """
    def __init__(self, screen, game_font, path, fast,  cell_width, cell_height):
        self._screen = screen
        self._game_font = game_font
        self._fast = fast
        self._cell_width = cell_width
        self._cell_height = cell_height
        self._grid = self.init_grid(path)

    @property
    def grid(self):
        return self._grid

    @grid.setter
    def grid(self, new_grid):
        self._grid = new_grid

    def init_grid(self, path):
        """Initialize a grid from a JSON file

        Args:
            path (str): Path to a JSON file containing the grid

        Returns:
            list: List of lists representing the current Sudoku game
        """
        grid = list()

        with open(path) as f:
            board_data = json.load(f)

        for row in range(len(board_data["board"])):
            grid.append(list())
            col_checker = 0

            for col, number in enumerate(board_data["board"]["row" + str(row + 1)]):
                grid[row].append(Cell(row, col, self._cell_width, self._cell_height, number))
                col_checker += 1

            if col_checker != len(board_data["board"]):
                print("Number of rows does not match number of columns. Please verify your Sudoku board at {path}".format(path=path))
                sys.exit(1)

        return grid

    def find_empty_position(self):
        """Find if a position in a given row/col is empty and return it

        Returns:
            tuple: row and col of an empty position or -1, -1 if no such position exists
            as well as True or False whether a number has been assigned to that position or not
        """
        empty_row = -1
        empty_col = -1

        for row in range(9):
            for col in range(9):
                if self._grid[row][col].solution == 0:
                    empty_row = row
                    empty_col = col
                    return empty_row, empty_col, False

        return empty_row, empty_col, True

    def move_is_safe(self, suggestion, row, col):
        """Check whether the suggestion move for the given row and col is safe to play
        by checking for the existence in the current row, current column, and current sub matrix

        Args:
            suggestion (int): The suggestion move to play
            row (int): Current row at which to place the suggestion
            col (int): Current col at which to place the suggestion

        Returns:
            bool: True whether a move with the current suggestion would be valid or not based on
                  the current state of the sudoky board
        """
        # Check current row
        for index in range(9):
            if self._grid[row][index].solution == suggestion:
                self._grid[row][col].color = Color.Background
                return False

        # Check current col
        for index in range(9):
            if self._grid[index][col].solution == suggestion:
                self._grid[row][col].color = Color.Background
                return False

        # Check current submatrix
        submat_row = (row // 3) * 3
        submat_col = (col // 3) * 3
        for sub_row in range(submat_row, submat_row + 3):
            for sub_col in range(submat_col, submat_col + 3):
                if self._grid[sub_row][sub_col].solution == suggestion:
                    self._grid[row][col].color = Color.Background
                    return False

        return True

    def solve_game(self):
        """Function that solved the sudoku board by using Backtracking

        Returns:
            Bool: True if the board can be solved, False otherwise
        """
        # Handle exiting while algo is running
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
        
        row, col, assigned = self.find_empty_position()

        if assigned:
            return True

        # Currently checking this row and col
        self._grid[row][col].color = Color.CurrentlySolving
        refresh_screen(self._screen, self, self._game_font)
        if not self._fast:
            pygame.time.wait(50)

        # Check for a valid solution between 1 and 9
        for suggestion in range(1, 10):
            if self.move_is_safe(suggestion, row, col):
                # Possible Solution
                self._grid[row][col].solution = suggestion
                self._grid[row][col].color = Color.Solved
                refresh_screen(self._screen, self, self._game_font)
                if not self._fast:
                    pygame.time.wait(50)

                # Continue with solution
                if self.solve_game():
                    return True

                # Backtrack
                self._grid[row][col].solution = 0
                self._grid[row][col].color = Color.Background
                refresh_screen(self._screen, self, self._game_font)
                if not self._fast:
                    pygame.time.wait(50)

        return False


def draw_grid_borders(screen, rows, cols, width, height):
    """Draws the borders of the Sudoku game

    Args:
        screen (pygame.display): The surface to draw the grid on
        rows (int): Sudoku rows
        cols (int): Sudoku cols
        width (int): Width of a single Sudoku cell
        height (int): Height of a single Sudoku cell

    Returns:
        list: All points that need to be redrawn by pygame due to a change.
              This way one saves resources and does not redraw the entire screen.
    """
    updated_points = list()

    for row in range(rows):
        line_width = 5 if row % 3 == 0 else 1

        dims1 = pygame.draw.line(screen, Color.Grid.value, (0, row * height), (width * rows, height * row), width=line_width)
        updated_points.append(dims1)

        for col in range(cols):
            line_width = 5 if col % 3 == 0 else 1

            dims2 = pygame.draw.line(screen, Color.Grid.value, (col * width, row * height), (col * width, row * height + height), width=line_width)
            updated_points.append(dims2)

    return updated_points


def refresh_screen(screen, game, game_font):
    """Function that redraws the screen at each iteration of the main event loop

    Args:
        screen (pygame.display): Surface to redraw the game on
        game (SudokuGame): Class representing a single instance of a Sudoku game
        game_font (pygame.freetype.Font): The font to use when rendering numbers in the Sudoku game
    """
    screen.fill(Color.Background.value)

    mid_point = 30
    updated_points = list()
    
    for row in range(9):
        for col in range(9):
            if game.grid[row][col].color != Color.Background:
                color = game.grid[row][col].color
                x = game.grid[row][col].xpos
                y = game.grid[row][col].ypos
                rect_dims = pygame.draw.rect(screen, color.value, (x, y, 90, 90))
                updated_points.append(rect_dims)
            
            text_surface, rect = game_font.render(str(game.grid[row][col]), Color.Text.value)
            rect = screen.blit(text_surface, pygame.Rect(col*90 + mid_point, row*90 + mid_point, 90, 90))
            updated_points.append(rect)

    updated_points += draw_grid_borders(screen, 9, 9, 90, 90)

    pygame.display.update(updated_points)


def main():
    parser = argparse.ArgumentParser(description="""Sudoku Solver using the Backtracking algorithm and pygame for visualizations.
    Usage instructions:
    1. Press space to initialize the algorithm.
    2. Press TAB to reset the board from the beginning.""", formatter_class=argparse.RawTextHelpFormatter)
    
    parser.add_argument('-p', '--path', dest='path', required=True, help='Path to a JSON file with a board to be solved')
    parser.add_argument('-f', '--fast', action='store_true', dest='fast', help='Whether to speed up animations or run slower')
    
    args = parser.parse_args()
    
    path = os.path.abspath(os.path.expanduser(args.path))
    fast = args.fast

    pygame.init()
    screen = pygame.display.set_mode((810, 810))
    pygame.display.set_caption("Sudoku Backtracking Solver")

    font_size = 48
    game_font = pygame.freetype.Font("./fonts/Fira Code Bold Nerd Font Complete.ttf", font_size)

    sudoku = SudokuGame(screen, game_font, path, fast, 90, 90)

    while True:
        refresh_screen(screen, sudoku, game_font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    sudoku.solve_game()

                if event.key == pygame.K_TAB:
                    sudoku = SudokuGame(screen, game_font, path, fast, 90, 90)

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # Sleep for x milliseconds to release the CPU to other processes
        pygame.time.wait(10)


if __name__ == "__main__":
    main()
