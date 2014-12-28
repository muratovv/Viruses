__author__ = 'muratov'
import itertools
import math

import pygame
import pygame.gfxdraw


class enumColor:
    """
    Описание цветов игрового поля
    """
    oddBlockColor = "#7EB044"
    evenBlockColor = "#519600"

    player1Color = "#750CE8"
    player2Color = "#990054"

    ripPlayer1Color = "#A99AB0"
    ripPlayer2Color = "#A9FFB0"

    fieldBackgroundColor = "#519600"


class enumFigures:
    """
    Типы фигур на игровом поле
    """
    player1 = "1"
    player2 = "2"
    ripPlayer1 = "*"
    ripPlayer2 = "#"
    empty = " "


class Level:
    """
    Карта уровня и его отрисовка
    """

    def __init__(self, screen, N):
        self.screen = screen
        self.levelMap = [[enumFigures.empty for x in range(N)] for x in range(N)]
        self.N = N
        self.colorGenerator = iter(itertools.cycle([enumColor.oddBlockColor, enumColor.evenBlockColor]))
        self.widthBlock = 0
        self.heightBlock = 0

    def drawLevel(self):
        size = self.screen.get_size()
        self.widthBlock = size[0] / self.N
        self.heightBlock = size[1] / self.N
        coordinates = [0, 0, self.widthBlock, self.heightBlock]
        if self.N % 2:
            color = next(self.colorGenerator)
        for column in range(self.N):
            if not self.N % 2:
                color = next(self.colorGenerator)
            for row in range(self.N):
                color = next(self.colorGenerator)
                coordinates[0] = column * self.widthBlock
                coordinates[1] = row * self.heightBlock
                pygame.draw.rect(self.screen, pygame.Color(color),
                                 coordinates)
        self.drawFigures()

    def drawFigures(self):
        playerMap = {enumFigures.player1: enumColor.player1Color, enumFigures.player2: enumColor.player2Color,
                     enumFigures.ripPlayer1: enumColor.ripPlayer1Color, enumFigures.ripPlayer2: enumColor.ripPlayer2Color}
        for i in range(self.N):
            for j in range(self.N):
                if self.levelMap[i][j] != enumFigures.empty:
                    self.drawFigure((j, i), playerMap[self.levelMap[i][j]])

    def drawFigure(self, point, color):
        rect = [int(point[0] * self.widthBlock), int(point[1] * self.heightBlock), self.widthBlock, self.heightBlock]
        pygame.draw.ellipse(self.screen, pygame.Color(color), rect)

    def transformMousePosToCells(self, mouseRelativePoint):
        return math.floor(mouseRelativePoint[0] / self.widthBlock), math.floor(mouseRelativePoint[1] / self.heightBlock)
