__author__ = 'muratov'

import random
import shelve
import GameLogic
from collections import defaultdict


class MachinePlayer:
    """
    Класс управляет ходами компьютера.
    makeMove - выдает позицию, на которую компьютер хочет поставить фишку.
    """

    def __init__(self, path, gameLvl):
        self.d = shelve.open(path)
        self.lvl = gameLvl
        if "goodMove" not in self.d:
            self.d["goodMove"] = []
        if "successLine" not in self.d:
            self.d["successLine"] = defaultdict(list)
        self.step = 0
        self.localHistory = defaultdict(list)
        self.eps = 0

    def makeMove(self, moves):
        try:
            goodMove = []
            for move in moves:
                if move in self.d["goodMove"]:
                    goodMove.append(move)
            for move in self.d["successLine"][self.step]:
                if move in moves:
                    goodMove.append(move)
            goodMove = list(set(goodMove))
            randChoice = random.choice(moves)
            if len(goodMove) > 0:
                choose = random.uniform(0, 1)
            else:
                choose = 0
            if choose > 0.5 - self.eps:
                move = random.choice(goodMove)
            else:
                move = randChoice
                self.trySaveRandMove(move)
                self.localHistory[self.step].append(move)
            return move
        except IndexError:
            return None


    def trySaveRandMove(self, move):
        if self.lvl.levelMap[move[1]][move[0]] == GameLogic.enumPlayers.player1[1]:
            if move not in self.d["goodMove"]:
                self.d["goodMove"].append(move)

    def flushHistory(self):
        for key in self.d["successLine"]:
            self.d["successLine"][key] += self.localHistory[key]

    def close(self):
        self.d.close()


