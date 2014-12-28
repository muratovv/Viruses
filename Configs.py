__author__ = 'muratov'

import sys

class Configuration:
    N = 5

    resolution = (800, 600)
    appName = "Вирусы"
    font = "monospace", 18
    backGroundColor = "#E6FF8A"
    gameFieldOffset = (0, 100)

    @staticmethod
    def getCommandLineArgs():
        try:
            N = int(sys.argv[1])
            if N < 5:
                raise ValueError("N < 5")
            else:
                Configuration.N = N
            if len(sys.argv) == 4:
                xRes = int(sys.argv[2])
                yRes = int(sys.argv[3])
                if xRes > 0 and yRes > 100:
                    Configuration.resolution = (xRes, yRes)
                else:
                    raise ValueError("Bad resolution")
            if len(sys.argv) == 3 or len(sys.argv) > 4:
                raise IndexError("wrong quantity of args")
        except (ValueError, IndexError) as ex:
            print(ex)

class EndGame(Exception):
    pass