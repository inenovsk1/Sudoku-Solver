#!/usr/bin/env python3
"""Sudoku Solver using Pygame and the backtracking algorithm
"""

import sys
import enum
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


class SudokuGame():
    """Class that implements the logic of solving Sudoku by using
    the Backtracking algorithm
    """
    #TODO: Implement the SudokuGame class
    def __init__(self, how='random'):
        pass
        # self._grid


class Cell():
    """Implementation of a single Sudoku cell. Use this class to keep track
    of a cell's color, coordinate positions, and current solution
    """
    def __init__(self, row, col, width, height):
        self._row = row
        self._col = col
        self._xpos = row * width
        self._ypos = col * height
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


def main():
    pygame.init()
    screen = pygame.display.set_mode((810, 810))
    pygame.display.set_caption("Sudoku Backtracking Solver")

    font_size = 48
    game_font = pygame.freetype.Font("./fonts/Fira Code Bold Nerd Font Complete.ttf", font_size)
    
    # The mid point of a single cell = (810 / 9) / 2. Use this to center the text when drawing
    mid_point = 45

    while True:
        screen.fill(Color.Background.value)
        
        for i in range(9):
            text_surface, rect = game_font.render(str(i + 1), Color.Text.value)
            screen.blit(text_surface, pygame.Rect(i * 90 + mid_point, 0 + mid_point, 90, 90))
            for k in range(1, 9):
                text_surface, rect = game_font.render(str(i + 1), Color.Text.value)
                screen.blit(text_surface, pygame.Rect(i*90 + mid_point, k*90 + mid_point, 90, 90))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

        pygame.display.update()


if __name__ == "__main__":
    main()
