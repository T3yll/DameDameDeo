import tkinter as tk

import game
import Pion


class GameBoard:
    def __init__(self):
        self.window = tk.Tk()
        self.canvas = tk.Canvas(self.window, width=800, height=800)
        self.cases = [[Pion.Pion(self.canvas, 0, 0, 0, 0, "black") for _ in range(10)] for _ in range(10)]
        self.game = game.Game()
        self.canvas.grid(row=1, column=1, padx=20, pady=20)
        self.canvas.bind("<Button-1>", self.selectPion)
        self.highlighted = []
        self.selectedPion = None
        self.selectedPionPosition = []
        self.square = 80
        for i, j in enumerate(self.game.grid):
            for k, l in enumerate(j):
                color = "brown" if (i + k) % 2 == 0 else "grey"
                self.canvas.create_rectangle(i * self.square, k * self.square, i * self.square + self.square,
                                             k * self.square + self.square, fill=color)
                if l == 1:
                    pion = Pion.Pion(self.canvas, i * self.square, k * self.square, i * self.square + self.square,
                                     k * self.square + self.square, "black", 5)
                    self.cases[i][k] = pion
                elif l == 2:
                    pion = Pion.Pion(self.canvas, i * self.square, k * self.square, i * self.square + self.square,
                                     k * self.square + self.square, "white", 5)
                    self.cases[i][k] = pion
                else:
                    self.cases[i][k] = None

        print(self.cases)

    def refreshGrid(self):

        """rafraichit l'affichage de la grille pour update la position des pions"""
        self.canvas.delete("all")
        for i, j in enumerate(self.game.grid):
            for k, l in enumerate(j):
                color = "brown" if (i + k) % 2 == 0 else "grey"
                self.canvas.create_rectangle(i * self.square, k * self.square, i * self.square + self.square,
                                             k * self.square + self.square, fill=color)
                if l == 1:
                    pion = Pion.Pion(self.canvas, i * self.square, k * self.square, i * self.square + self.square,
                                     k * self.square + self.square, "black", 5)
                    self.cases[i][k] = pion
                elif l == 2:
                    pion = Pion.Pion(self.canvas, i * self.square, k * self.square, i * self.square + self.square,
                                     k * self.square + self.square, "white", 5)
                    self.cases[i][k] = pion
                else:
                    self.cases[i][k] = None

    def selectPion(self, event):
        """selectione un pion sur le plateau"""
        # self.print()
        for x, row in enumerate(self.cases):
            for y, cell in enumerate(row):
                if cell == None and [x, y] in self.highlighted and (
                        event.x > x * self.square and event.x < (x + 1) * self.square) and (
                        event.y > y * self.square and event.y < (y + 1) * self.square):
                    self.tryPlay(x, y)
                if cell != None and (event.x > cell.x1 and event.x < cell.x2) and (
                        event.y > cell.y1 and event.y < cell.y2):
                    print("Pion selected")
                    posToPlay = self.isPlayable(x, y)
                    if posToPlay == False:
                        self.deleteHighlighted()
                    elif not len(posToPlay) == 0:
                        for i in posToPlay:
                            self.canvas.create_rectangle(i[0] * 80, i[1] * 80, i[0] * 80 + 80, i[1] * 80 + 80,
                                                         fill="blue")
                            self.highlighted.append([i[0], i[1]])

    def deleteHighlighted(self):
        """Permet de supprimer les carré bleus qui apparaissent lorsqu'on clique sur un pion"""
        for i in self.highlighted:
            self.canvas.create_rectangle(i[0] * 80, i[1] * 80, i[0] * 80 + 80, i[1] * 80 + 80, fill="brown")
        self.highlighted = []

    def isPlayable(self, posX, posY):
        """verifie si une piece a la position posX and posY peut jouer
         et renvoie une liste des coups disponibles ou false si la piece est deja selectionnéé"""
        print(int(posX))
        self.deleteHighlighted()
        self.selectedPion = self.cases[posX][posY]
        self.selectedPionPosition = [posX, posY]
        toret = []
        if not (posX == 0 or posX == 9):
            if self.game.grid[posX - 1][posY - 1] == 0:
                if [posX - 1, posY - 1] in self.highlighted:
                    return False
                toret.append([posX - 1, posY - 1])
            if self.game.grid[posX + 1][posY - 1] == 0:
                if [posX + 1, posY - 1] in self.highlighted:
                    return False
                toret.append([posX + 1, posY - 1])
            return toret

        else:
            if posX == 9 and self.game.grid[posX - 1][posY - 1] == 0:
                if [posX - 1, posY - 1] in self.highlighted:
                    return False
                return [[posX - 1, posY - 1]]
            elif posX == 0 and self.game.grid[posX + 1][posY - 1] == 0:
                if [posX + 1, posY - 1] in self.highlighted:
                    return False
                return [[posX + 1, posY - 1]]
            else:
                return []

    def tryPlay(self, posX, posY):
        """Essaie de jouer a la position posX,posY dans la grille de jeu
                @:parameter posX: Position X dans la grille de jeu
                @:parameter posY: Position Y dans la grille de jeu
                @return: True si le pion a bougé
                @return: False sinon
                """
        print("ici")
        if self.selectedPion == None:
            print("TG")
            return False
        if [posX, posY] in self.highlighted:
            self.cases[posX][posY] = self.selectedPion
            self.game.grid[posX][posY] = 2
            self.game.grid[self.selectedPionPosition[0]][self.selectedPionPosition[1]] = 0
            print("deplace")
            self.refreshGrid()
            self.highlighted = []
            return True

    def print(self):
        for row in self.cases:
            print(row)



if __name__ == '__main__':
    game = GameBoard()
    game.window.mainloop()
