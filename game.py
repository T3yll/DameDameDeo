import random

import numpy as np


class Game:
    def __init__(self):
        self.grid = [[0 for x in range(10)] for y in range(10)]
        self.tour = 1
        self.current = random.choice([1, 2])
        self.placeBegin()

    def placeBegin(self,debug=False):
        if debug:
            self.grid=[[1,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],
                       [0,0,2,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0,0,0]]
            return
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

    def isEnd(self):
        tmp = np.unique(np.array(self.grid).flatten())
        if len(tmp) == 2:
            return np.delete(tmp, 0)[0]
        return False

    def changePlayer(self):
        if self.isEnd():
            return False
        print("wedfwe")
        self.current = 2 if self.current == 1 else 1
        self.tour += 1
        return True

    def print(self):
        for i, j in enumerate(self.grid):
            print(j)

    def getCurrent(self):
        return self.current
    
    def setCurrent(self,current):
        self.current = current