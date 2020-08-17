#!/usr/bin/env python3
"""Sudoku Solver using Pygame and the backtracking algorithm
"""

import sys
import pygame


class SudokuGame():
    def __init__(self):
        pass


def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Sudoku Backtracking Solver")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)


if __name__ == "__main__":
    main()
