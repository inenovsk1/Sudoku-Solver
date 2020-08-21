#!/usr/bin/env python3
"""Sudoku Solver using Pygame and the backtracking algorithm
"""

import sys
import enum
import json
import pygame
import pygame.freetype


class Color(enum.Enum):
    Background = (38, 49, 50)
    Foreground = (237, 238, 237)
    Text = (255, 255, 255)
    CurrentlySolving = (255, 81, 81)
    Solved = (105, 240, 173)
    Unsolved = Background
    Grid = (96, 124, 139)


class Cell():
    """Implementation of a single Sudoku cell. Use this class to keep track
    of a cell's color, coordinate positions, and current solution
    """
    def __init__(self, row, col, width, height, number):
        self._row = row
        self._col = col
        self._xpos = row * width
        self._ypos = col * height

        if number:
            self._solution = number
            self._color = Color.Solved
        else:
            self._solution = float("inf")
            self._color = Color.Unsolved

    @property
    def solution(self):
        return self._solution

    @solution.setter
    def solution(self, num):
        self,_solution = num

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, new_color):
        self._color = new_color


class SudokuGame():
    """Class that implements the logic of solving Sudoku by using
    the Backtracking algorithm
    """
    #TODO: Implement the SudokuGame class
    def __init__(self, path, cell_width, cell_height):
        self._grid = self.init_grid(path)
        self._cell_width = cell_width
        self._cell_height = cell_height

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

        for row in range(9):
            grid.append(list())
            for col, number in enumerate(board_data["board"]["row" + str(row + 1)]):
                grid[row].append(Cell(row, col, self._cell_width, self._cell_height, number))

        return grid


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


def main():
    pygame.init()
    screen = pygame.display.set_mode((810, 810))
    pygame.display.set_caption("Sudoku Backtracking Solver")

    font_size = 48
    game_font = pygame.freetype.Font("./fonts/Fira Code Bold Nerd Font Complete.ttf", font_size)
    
    # The mid point of a single cell = (810 / 9) / 2. Use this to center the text when drawing
    mid_point = 30

    while True:
        screen.fill(Color.Background.value)
        
        for i in range(9):
            text_surface, rect = game_font.render(str(i + 1), Color.Text.value)
            screen.blit(text_surface, pygame.Rect(i * 90 + mid_point, 0 + mid_point, 90, 90))
            for k in range(1, 9):
                text_surface, rect = game_font.render(str(i + 1), Color.Text.value)
                screen.blit(text_surface, pygame.Rect(i*90 + mid_point, k*90 + mid_point, 90, 90))

        draw_grid_borders(screen, 9, 9, 90, 90)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

        pygame.display.update()


if __name__ == "__main__":
    main()
