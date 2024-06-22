import tkinter as tk

import game
import Pion


class GameBoard:
    def __init__(self):
        self.window = tk.Tk()
        self.canvas = tk.Canvas(self.window, width=800, height=800)
        self.cases = [[None for i in range(10)] for j in range(10)]
        self.game = game.Game()
        self.canvas.grid(row=1, column=1, padx=20, pady=20)
        self.canvas.bind("<Button-1>", self.selectPion)
        self.highlighted = []
        self.canEat = {}
        self.selectedPion = None
        self.selectedPionPosition = []
        self.square = 80

        self.refreshGrid()

       # print(self.cases)

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
                                     k * self.square + self.square, "black", 1)
                    self.cases[i][k] = pion
                elif l == 2:
                    pion = Pion.Pion(self.canvas, i * self.square, k * self.square, i * self.square + self.square,
                                     k * self.square + self.square, "white", 2)
                    self.cases[i][k] = pion
                else:
                    self.cases[i][k] = None

    def selectPion(self, event):
        """selectione un pion sur le plateau"""
        #self.print()
        for x, row in enumerate(self.cases):
            for y, cell in enumerate(row):
                if cell == None and [x, y] in self.highlighted and (event.x > x * self.square and event.x < (x + 1) * self.square) and (event.y > y * self.square and event.y < (y + 1) * self.square):
                    self.tryPlay(x, y)
                if cell != None and (event.x > cell.x1 and event.x < cell.x2) and (event.y > cell.y1 and event.y < cell.y2) and cell.team == self.game.current:
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
        self.canEat = {}



    def isPlayable(self, posX, posY):
        """verifie si une piece a la position posX and posY peut jouer
         et renvoie une liste des coups disponibles ou false si la piece est deja selectionnéé"""
        #print(int(posX))
        self.deleteHighlighted()
        self.selectedPion = self.cases[posX][posY]
        self.selectedPionPosition = [posX, posY]
        deplacement= -1 if (self.selectedPion.team==1) else 1
        toret = []
        other_team = 2 if (self.selectedPion.team==1) else 1
        if not (posX == 0 or posX == 9):
            if self.game.grid[posX - 1][posY - deplacement] == 0:
                if [posX - 1, posY - deplacement] in self.highlighted:
                    return False
                toret.append([posX - 1, posY - deplacement])
            if self.game.grid[posX + 1][posY - deplacement] == 0:
                if [posX + 1, posY - deplacement] in self.highlighted:
                    return False
                toret.append([posX + 1, posY - deplacement])

            if (not posX == 0) and self.game.grid[posX - 1][posY - deplacement] == other_team and self.game.grid[posX - 2][posY - 2 * deplacement] == 0:
                self.canEat[str((posX - 2,posY - 2 * deplacement))]=(posX - 1,posY - deplacement)
                toret.append([posX - 2, posY - 2 * deplacement])

            if (not posX == 8) and self.game.grid[posX + 1][posY - deplacement] == other_team and self.game.grid[posX + 2][posY - 2 * deplacement] == 0:
                self.canEat[str((posX + 2,posY - 2 * deplacement))]=(posX + 1,posY - deplacement)
                toret.append([posX + 2, posY - 2 * deplacement])
            return toret
        else:
            if posX == 9 and self.game.grid[posX - 1][posY - deplacement] == 0:
                if [posX - 1, posY - deplacement] in self.highlighted:
                    return False
                return [[posX - 1, posY - deplacement]]
            elif posX == 0 and self.game.grid[posX + 1][posY - deplacement] == 0:
                if [posX + 1, posY - deplacement] in self.highlighted:
                    return False
                return  [[posX + 1, posY - deplacement]]
            if posX == 9 and self.game.grid[posX - 1][posY - deplacement] == other_team and self.game.grid[posX - 2][posY - 2 * deplacement] == 0:
                self.canEat[str((posX - 2,posY - 2 * deplacement))]=(posX - 1,posY - deplacement)
                return [[posX - 2, posY - 2 * deplacement]]
            if posX == 0 and self.game.grid[posX + 1][posY - deplacement] == other_team and self.game.grid[posX + 2][posY - 2 * deplacement] == 0:
                self.canEat[str((posX + 2,posY - 2 * deplacement))]=(posX + 1,posY - deplacement)
                return [[posX + 2, posY - 2 * deplacement]]
            else:
                return toret

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
        if [posX, posY] in self.highlighted: #le bout de code suivant sert a jouer le coup

            if str((posX, posY)) in self.canEat.keys():
                key=str((posX, posY))
                self.game.grid[self.canEat[key][0]][self.canEat[key][1]]=0
                self.cases[self.canEat[key][0]][self.canEat[key][1]] = None
            #print(self.canEat)
            self.cases[posX][posY] = self.selectedPion
            self.game.grid[posX][posY] = self.selectedPion.team
            self.game.grid[self.selectedPionPosition[0]][self.selectedPionPosition[1]] = 0
            self.refreshGrid()
            self.highlighted = []
            self.canEat = {}
            self.game.changePlayer()
            print(self.game.tour)
            self.print()


            if not self.game.isEnd() == False:
                print("finito")
            return True



    def print(self):
        for row in self.cases:
            toprint= []
            for cell in row:
                if cell != None:
                    toprint.append(cell.team)
                else:
                    toprint.append(0)
            print(toprint)



if __name__ == '__main__':
    game = GameBoard()
    game.window.mainloop()
