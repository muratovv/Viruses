__author__ = 'muratov'
import pygame
import Configs



class Indicator:
    """
    Игровой индикатор
    """
    HUDs = dict()
    def __init__(self, screen, font, template, StartPoint):
        self.point = StartPoint
        self.screen = screen
        self.template = self.text = template
        self.font = font

    def show(self):
        if self.text:
            label1 = self.font.render(self.text, 2, pygame.Color(Configs.HudColor.hudColor))
            self.screen.blit(label1, self.point)

    def template(self, template):
        self.text = template

    def changeText(self, *args):
        self.text = self.template.format(*args)