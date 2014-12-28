#!/usr/bin/env python3
"""
Есть поле NxN и два игрока. За первого играет пользователь, за второго - компьютер.
Изначально у игроков выставлено на поле по 5 фишек.(у одного игрока произвольно в нижнем ряду, у другого - в верхнем).
Ход игрока состоит из 5 действий. Каждое действие это либо постановка нового вируса, либо убийство противника. При этом ставить вирус или убивать противника в какой-либо клетке можно при условии, что либо с этой клеткой напрямую (по диагонали тоже можно) граничит ваш вирус, либо есть цепочка из убитых _вами_ вирусов, соединяющая эту клетку с каким либо вашим вирусом.
"""

__author__ = 'muratov'
import pygame
import sys
import Level
import GameLogic
import Player
from Configs import Configuration as conf
from Indicator import Indicator


def init():
    conf.init()


def initHUD():
    Indicator.HUDs["score"] = Indicator(conf.screen, conf.gameFont, "Score", (10, 10))
    Indicator.HUDs["player"] = Indicator(conf.screen, conf.gameFont, "player {0}", (10, 30))
    Indicator.HUDs["computer"] = Indicator(conf.screen, conf.gameFont, "computer {0}", (10, 50))
    Indicator.HUDs["move"] = Indicator(conf.screen, conf.gameFont, "move {0}, remaining steps {1}", (300, 10))


def init():
    pygame.init()
    conf.gameFont = pygame.font.SysFont(*conf.font)
    conf.screen = pygame.display.set_mode(conf.resolution)
    pygame.display.set_caption(conf.appName)


def mainLoop():
    pygame.init()
    init()
    initHUD()
    clock = pygame.time.Clock()
    Indicator.HUDs["computer"].changeText(0)
    Indicator.HUDs["player"].changeText(0)
    bg = pygame.Surface(conf.resolution)
    bg.fill(pygame.Color(conf.backGroundColor))
    gameField = pygame.Surface((conf.resolution[0] - conf.gameFieldOffset[0], conf.resolution[1] - conf.gameFieldOffset[1]))
    gameField.fill(pygame.Color(Level.enumColor.fieldBackgroundColor))
    lvl = Level.Level(gameField, conf.N)
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
        if logic.exitState[0]:
            return logic.exitState[1]



        # show block
        conf.screen.blit(bg, (0, 0))
        conf.screen.blit(gameField, conf.gameFieldOffset)
        lvl.drawLevel()
        for hud in Indicator.HUDs.values():
            hud.show()
        pygame.display.update()
        clock.tick(100)


if __name__ == '__main__':
    conf.getCommandLineArgs()
    try:
        m = mainLoop()
        print(m)
    except Exception as ex:
        print(ex)