import random

import numpy as np


class Game:
    def __init__(self,isVirtual=False):
        self.grid = [[0 for x in range(10)] for y in range(10)]
        self.tour = 1
        self.current = random.choice([1, 2])
        self.placeBegin()

    def placeBegin(self):
        current = 1
        for i, j in enumerate(self.grid):
            for k, l in enumerate(j):
                if k == 4 or k == 5:
                    continue
                if k >= 5:
                    current = 2
                else:
                    current = 1
                if i % 2 == 0:
                    if k % 2 == 0:
                        self.grid[i][k] = current
                else:
                    if k % 2 == 1:
                        self.grid[i][k] = current
        self.print()

    def isEnd(self):
        tmp = np.unique(np.array(self.grid).flatten())
        if len(tmp) == 2:
            return np.delete(tmp, 0)[0]
        return False

    def changePlayer(self):
        print("wedfwe")
        self.current = 2 if self.current == 1 else 1
        self.tour += 1
        return

    def print(self):
        for i, j in enumerate(self.grid):
            print(j)
