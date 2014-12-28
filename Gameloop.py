#!/usr/bin/env python3
__author__ = 'muratov'
import sys

import pygame

import Level
import Hud
import GameLogic
import Player

screen = None
gameFont = None
HUDs = dict()

N = 5
resolution = (800, 600)


def getCommandLineArgs():
    try:
        global N
        N = int(sys.argv[1])
        if N < 5:
            N = 5
    except:
        pass


def init():
    pygame.init()
    global gameFont, screen
    gameFont = pygame.font.SysFont("monospace", 18)
    screen = pygame.display.set_mode(resolution)
    pygame.display.set_caption("Вирусы")


def initHUD():
    HUDs["score"] = Hud.Hud(screen, gameFont, "Score", (10, 10))
    HUDs["player"] = Hud.Hud(screen, gameFont, "player {0}", (10, 30))
    HUDs["computer"] = Hud.Hud(screen, gameFont, "computer {0}", (10, 50))
    HUDs["move"] = Hud.Hud(screen, gameFont, "move {0}, remaining steps {1}", (300, 10))

    # HUDs["mouse"] = Hud.Hud(screen, gameFont, "mouse at {0}, {1}", (10, 70))


def mainLoop():
    init()
    initHUD()
    clock = pygame.time.Clock()
    HUDs["computer"].changeText(0)
    HUDs["player"].changeText(0)
    bg = pygame.Surface(resolution)
    bg.fill(pygame.Color("#E6FF8A"))
    gameFieldPos = (0, 100)
    gameField = pygame.Surface((resolution[0] - gameFieldPos[0], resolution[1] - gameFieldPos[1]))
    gameField.fill(pygame.Color("#519600"))
    lvl = Level.Level(gameField, 10)
    logic = GameLogic.gameLogic(lvl)
    machine = Player.MachinePlayer("base", lvl)

    while True:
        # event block
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                raise SystemExit("quit")
            if e.type == pygame.MOUSEBUTTONDOWN:
                if logic.activePlayer[0] == GameLogic.enumControlType.human:
                    pos = pygame.mouse.get_pos()
                    relativePos = (pos[0] - gameFieldPos[0], pos[1] - gameFieldPos[1])
                    move = lvl.transformMousePosToCells(relativePos)
                    # HUDs["mouse"].changeText(*move)
                    logic.makeMove(move)


        # update block
        HUDs["move"].changeText(*logic.getInfo())
        for key in logic.state["score"]:
            HUDs[key].changeText(logic.state["score"][key])
        if logic.activePlayer[0] == GameLogic.enumControlType.machine:
            move = machine.makeMove(logic.state["moves"])
            logic.makeMove(move)



        # show block
        screen.blit(bg, (0, 0))
        screen.blit(gameField, gameFieldPos)
        lvl.drawLevel()
        for hud in HUDs.values():
            hud.show()
        pygame.display.update()
        clock.tick(100)


if __name__ == '__main__':
    getCommandLineArgs()
    try:
        mainLoop()
    except GameLogic.EndGame as ex:
        print(ex)