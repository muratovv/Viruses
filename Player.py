__author__ = 'muratov'

import random
import shelve
import GameLogic

class MachinePlayer:
    def __init__(self, path, gameLvl):
        self.d = shelve.open(path)
        self.lvl = gameLvl
        if "goodMove" not in self.d:
            self.d["goodMove"] = []

    def makeMove(self, moves):
        try:
            goodMove = []
            for move in moves:
                if move in self.d["goodMove"]:
                    goodMove.append(move)
            randChoice = random.choice(moves)

            if len(goodMove) > 0:
                choose = random.choice([1, 2])
                if choose == 1:
                    return random.choice(goodMove)
            return randChoice
        except IndexError:
            return None

    def trySaveRandMove(self, move):
        if self.lvl.levelmap[move[1]][move[0]] == GameLogic.enumStates.player1[1]:
            if move not in self.d["goodMove"]:
                self.d["goodMove"].append(move)
