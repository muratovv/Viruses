__author__ = 'muratov'

import Level
from collections import defaultdict
import random


class EndGame(Exception):
    pass


class enumControlType:
    machine = "machine"
    human = "human"


class enumStates:
    """
    0 - тип управления
    1 - имя
    2 - тип фигур
    3 - оставляет после убийства
    """
    player1 = (enumControlType.human, "player", Level.enumFigures.player1, Level.enumFigures.ripPlayer2)
    player2 = (enumControlType.machine, "computer", Level.enumFigures.player2, Level.enumFigures.ripPlayer1)


class gameLogic:
    maxTurns = 5

    def __init__(self, lvl):
        self.level = lvl
        self.locateStartViruses()
        self.players = [enumStates.player1, enumStates.player2]
        self.activePlayer = self.getStartPlayer()
        self.turns = gameLogic.maxTurns
        self.nextState()
        self.turns += 1

    def getInfo(self):
        return self.activePlayer[1], self.turns

    def locateStartViruses(self):
        startViruses = 5

        player1 = [Level.enumFigures.player1 for x in range(startViruses)] + \
                  [Level.enumFigures.empty for x in range(self.level.N - startViruses)]
        random.shuffle(player1)

        player2 = [Level.enumFigures.player2 for x in range(startViruses)] + \
                  [Level.enumFigures.empty for x in range(self.level.N - startViruses)]
        random.shuffle(player2)

        self.level.levelMap[0] = player2
        self.level.levelMap[self.level.N - 1] = player1

    def getStartPlayer(self):
        return random.choice(self.players)

    def availableMoves(self, player):
        """
        player - константа из level
        """
        markers = [self.activePlayer[2], self.activePlayer[3]]
        moves = []
        for column in range(self.level.N):
            for row in range(self.level.N):
                if self.level.levelMap[column][row] == player:
                    self.movesFromPoint(markers, (row, column), moves)
        v1 = list()
        for num in range(len(moves)):
            cell = moves[num]
            if self.level.levelMap[cell[1]][cell[0]] != self.activePlayer[3]:
                v1.append(cell)
            visited = v1
        return moves

    def movesFromPoint(self, markers, point, visited):
        """
        :param point: dot (x, y)
        """
        p = point
        tour = [(p[0] - 1, p[1] - 1), (p[0], p[1] - 1), (p[0] + 1, p[1] - 1),
                (p[0] - 1, p[1]),                           (p[0] + 1, p[1]),
                (p[0] - 1, p[1] + 1), (p[0], p[1] + 1), (p[0] + 1, p[1] + 1)]
        for cell in tour:
            try:
                if cell not in visited:
                    if 0 <= cell[0] < self.level.N and 0 <= cell[1] < self.level.N:
                        if self.activePlayer[2] == Level.enumFigures.player2:
                            enemy = Level.enumFigures.player1
                        else:
                            enemy = Level.enumFigures.player2
                        if self.level.levelMap[cell[1]][cell[0]] in [Level.enumFigures.empty, enemy]:
                            visited.append(cell)
                        else:

                            if self.level.levelMap[cell[1]][cell[0]] == self.activePlayer[3]:
                                visited.append(cell)
                                self.movesFromPoint(markers, cell, visited)

            except IndexError:
                pass





    def updateScore(self):
        d = defaultdict(int)
        for i in range(self.level.N):
            for j in range(self.level.N):
                if self.level.levelMap[i][j] == enumStates.player1[2]:
                    d[enumStates.player1[1]] += 1
                elif self.level.levelMap[i][j] == enumStates.player2[2]:
                    d[enumStates.player2[1]] += 1
        return d

    def nextState(self):

        if self.turns == 1:
            self.turns = gameLogic.maxTurns
            if self.activePlayer == self.players[0]:
                self.activePlayer = self.players[1]
            else:
                self.activePlayer = self.players[0]
        else:
            self.turns -= 1
        stateDict = {"score": self.updateScore(),
                     "player": self.activePlayer,
                     "moves": self.availableMoves(self.activePlayer[2])}
        if len(stateDict["moves"]) == 0:
            winner = None
            if self.activePlayer == self.players[0]:
                winner = self.players[1]
            else:
                winner = self.players[0]
            raise EndGame("Win {0}".format(winner[1]))
        else:
            for key in stateDict["score"]:
                if stateDict["score"][key] == 0:
                    if self.activePlayer == self.players[0]:
                        winner = self.players[1]
                    else:
                        winner = self.players[0]
                    raise EndGame("Win {0}".format(winner[1]))
        self.state = stateDict
        # print("nextState", self.state)

    def makeMove(self, move):
        # print("makeMove", move)
        if self.state is not None:
            if move in self.state["moves"]:
                if self.level.levelMap[move[1]][move[0]] == self.activePlayer[3]:
                    return
                if self.level.levelMap[move[1]][move[0]] == Level.enumFigures.empty:
                    self.level.levelMap[move[1]][move[0]] = self.activePlayer[2]
                else:
                    enemy = Level.enumFigures.player1 if self.activePlayer[2] == Level.enumFigures.player2 else Level.enumFigures.player2
                    if self.level.levelMap[move[1]][move[0]] == enemy:
                        self.level.levelMap[move[1]][move[0]] = self.activePlayer[3]

                self.nextState()