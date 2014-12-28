#!/usr/bin/env python3
"""
Задачка будет такая - написать игру Вирусы с ИИ (обучающимся на игроках).
Вирусы это такая игра - есть поле NxN. Изначально у игроков выставлено на поле по 5 вирусов (у одного игрока произвольно в нижнем ряду, у другого - в верхнем). Ход игрока состоит из 5 действий. Каждое действие это либо постановка нового вируса, либо убийство противника. При этом ставить вирус или убивать противника в какой-либо клетке можно при условии, что либо с этой клеткой напрямую (по диагонали тоже можно) граничит ваш вирус, либо есть цепочка из убитых _вами_ вирусов, соединяющая эту клетку с каким либо вашим вирусом.
"""

__author__ = 'muratov'
import pygame
import sys
import Level
import GameLogic
import Player
from Configs import Configuration as conf, EndGame
from Indicator import Indicator


def init():
    pygame.init()
    global gameFont, screen
    gameFont = pygame.font.SysFont(*conf.font)
    screen = pygame.display.set_mode(conf.resolution)
    pygame.display.set_caption(conf.appName)


def initHUD():
    Indicator.HUDs["score"] = Indicator(screen, gameFont, "Score", (10, 10))
    Indicator.HUDs["player"] = Indicator(screen, gameFont, "player {0}", (10, 30))
    Indicator.HUDs["computer"] = Indicator(screen, gameFont, "computer {0}", (10, 50))
    Indicator.HUDs["move"] = Indicator(screen, gameFont, "move {0}, remaining steps {1}", (300, 10))


def mainLoop():
    init()
    initHUD()
    clock = pygame.time.Clock()
    Indicator.HUDs["computer"].changeText(0)
    Indicator.HUDs["player"].changeText(0)
    bg = pygame.Surface(conf.resolution)
    bg.fill(pygame.Color(conf.backGroundColor))
    gameField = pygame.Surface((conf.resolution[0] - conf.gameFieldOffset[0], conf.resolution[1] - conf.gameFieldOffset[1]))
    gameField.fill(pygame.Color(Level.enumColor.fieldBackgroundColor))
    lvl = Level.Level(gameField, 10)
    logic = GameLogic.gameLogic(lvl)
    machine = Player.MachinePlayer("base", lvl)

    while True:
        # event block
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit(0)
            if e.type == pygame.MOUSEBUTTONDOWN:
                if logic.activePlayer[0] == GameLogic.enumControlType.human:
                    pos = pygame.mouse.get_pos()
                    relativePos = (pos[0] - conf.gameFieldOffset[0], pos[1] - conf.gameFieldOffset[1])
                    move = lvl.transformMousePosToCells(relativePos)
                    logic.makeMove(move)


        # update block
        Indicator.HUDs["move"].changeText(*logic.getInfo())
        for key in logic.state["score"]:
            Indicator.HUDs[key].changeText(logic.state["score"][key])
        if logic.activePlayer[0] == GameLogic.enumControlType.machine:
            move = machine.makeMove(logic.state["moves"])
            logic.makeMove(move)



        # show block
        screen.blit(bg, (0, 0))
        screen.blit(gameField, conf.gameFieldOffset)
        lvl.drawLevel()
        for hud in Indicator.HUDs.values():
            hud.show()
        pygame.display.update()
        clock.tick(100)


if __name__ == '__main__':
    conf.getCommandLineArgs()
    try:
        mainLoop()
    except EndGame as ex:
        print(ex)