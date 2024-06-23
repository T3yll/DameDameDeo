import tkinter as tk

import game as G
import Pion


class GameBoard:
    def __init__(self,isVirtual=False):
        if isVirtual==False:
            self.window = tk.Tk()
            self.canvas = tk.Canvas(self.window, width=800, height=800)
            self.canvas.grid(row=1, column=1, padx=20, pady=20)
            self.canvas.bind("<Button-1>", self.selectPion)
        self.cases = [[None for i in range(10)] for j in range(10)]
        self.game = G.Game(isVirtual=True)

        self.highlighted = []
        self.canEat = {}
        self.selectedPion = None
        self.selectedPionPosition = []
        self.square = 80
        if isVirtual == False:
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


    def canPlayRecursively(self,x,y,current):
        print("et moi et moi ?")
        for i in current:
            i=eval(i)
            virtualBoard = GameBoard(isVirtual=True)
            virtualBoard.cases=self.cases
            virtualBoard.game=self.game
            virtualBoard.selectedPion=virtualBoard.cases[x][y]
            virtualBoard.tryPlay(i[0],i[1],isVirtual=True)
            tmp = virtualBoard.isPlayableVirtual(i[0],i[1])
            if tmp is not False:
                print("recur")
                self.canEat.update(virtualBoard.canEat)
                return tmp
        return False

    def isPlayableVirtual(self,posX, posY):
        grid=self.game.grid
        deplacement = -1 if (self.selectedPion.team == 1) else 1
        other_team = 2 if (self.selectedPion.team == 1) else 1
        toret=[]
        if (not posX == 0) and grid[posX - 1][posY - deplacement] == other_team and grid[posX - 2][
            posY - 2 * deplacement] == 0:
            if str((posX - 2, posY - 2 * deplacement)) not in self.canEat:
                self.canEat[str((posX, posY))]=[(posX - 1, posY - deplacement)]
            else:
                self.canEat[str((posX,posY))].append((posX - 1, posY - deplacement))
            toret.append([posX - 2, posY - 2 * deplacement])

        if (not posX == 0) and grid[posX - 1][posY + deplacement] == other_team and grid[posX - 2][
            posY + 2 * deplacement] == 0:
            if str((posX - 2, posY + 2 * deplacement)) not in self.canEat:
                self.canEat[str((posX, posY))] = [(posX - 1, posY + deplacement)]
            else:
                self.canEat[str((posX, posY))].append((posX - 1, posY + deplacement))
            toret.append([posX - 2, posY + 2 * deplacement])

        if (not posX == 8) and grid[posX + 1][posY - deplacement] == other_team and grid[posX + 2][
            posY - 2 * deplacement] == 0:
            if str((posX + 2, posY - 2 * deplacement))  not in self.canEat:
                self.canEat[str((posX, posY))] = [(posX + 1, posY - deplacement)]
            else:
                self.canEat[str((posX, posY))].append((posX + 1, posY - deplacement))
            toret.append([posX + 2, posY - 2 * deplacement])

        if (not posX == 8) and grid[posX + 1][posY + deplacement] == other_team and grid[posX + 2][
            posY + 2 * deplacement] == 0:
            if str((posX + 2, posY + 2 * deplacement)) not in self.canEat:
                self.canEat[str((posX, posY))] = [(posX + 1, posY + deplacement)]
            else:
                self.canEat[str((posX, posY))].append((posX + 1, posY + deplacement))
            toret.append([posX + 2, posY + 2 * deplacement])
        return toret


    def isPlayable(self, posX, posY):
        """verifie si une piece a la position posX and posY peut jouer
         et renvoie une liste des coups disponibles ou false si la piece est deja selectionnéé"""
        #print(int(posX))
        grid = self.game.grid
        cases = self.cases
        self.deleteHighlighted()
        self.selectedPion = cases[posX][posY]
        self.selectedPionPosition = [posX, posY]
        print(posX,posY)
        print(self.canEat)
        deplacement= -1 if (self.selectedPion.team==1) else 1
        toret = []
        other_team = 2 if (self.selectedPion.team==1) else 1
        if not (posX == 0 or posX == 9):
            if grid[posX - 1][posY - deplacement] == 0:
                if [posX - 1, posY - deplacement] in self.highlighted:
                    return False
                toret.append([posX - 1, posY - deplacement])
            if grid[posX + 1][posY - deplacement] == 0:
                if [posX + 1, posY - deplacement] in self.highlighted:
                    return False
                toret.append([posX + 1, posY - deplacement])

            if (not posX == 0) and grid[posX - 1][posY - deplacement] == other_team and grid[posX - 2][posY - 2 * deplacement] == 0:
                if str((posX - 2,posY - 2 * deplacement)) not in self.canEat.keys():
                    self.canEat[str((posX - 2,posY - 2 * deplacement))]=[(posX - 1,posY - deplacement)]
                else:
                    self.canEat[str((posX - 2, posY - 2 * deplacement))].append((posX - 1, posY - deplacement))
                toret.append([posX - 2, posY - 2 * deplacement])

            if (not posX == 0) and grid[posX - 1][posY + deplacement] == other_team and grid[posX - 2][posY + 2 * deplacement] == 0:
                if str((posX - 2, posY + 2 * deplacement)) not in self.canEat.keys():
                    self.canEat[str((posX - 2, posY + 2 * deplacement))]=[(posX - 1, posY + deplacement)]
                else:
                    self.canEat[str((posX - 2, posY + 2 * deplacement))].append((posX - 1, posY + deplacement))
                toret.append([posX - 2, posY + 2 * deplacement])

            if (not posX == 8) and grid[posX + 1][posY - deplacement] == other_team and grid[posX + 2][posY - 2 * deplacement] == 0:
                if str((posX + 2,posY - 2 * deplacement)) not in self.canEat.keys():
                    self.canEat[str((posX + 2,posY - 2 * deplacement))]=[(posX + 1,posY - deplacement)]
                else:
                    self.canEat[str((posX + 2,posY - 2 * deplacement))].append((posX + 1,posY - deplacement))
                toret.append([posX + 2, posY - 2 * deplacement])

            if (not posX == 8) and grid[posX + 1][posY + deplacement] == other_team and grid[posX + 2][posY + 2 * deplacement] == 0:
                if str((posX + 2, posY + 2 * deplacement)) not in self.canEat.keys():
                    self.canEat[str((posX + 2, posY + 2 * deplacement))]=[(posX + 1, posY + deplacement)]
                else:
                    self.canEat[str((posX + 2,posY - 2 * deplacement))].append((posX + 1, posY + deplacement))
                toret.append([posX + 2, posY + 2 * deplacement])
            if len(self.canEat) != 0:
                recur = self.canPlayRecursively(posX, posY, self.canEat.keys())
                toret.extend(recur)
            return toret
        else: #si collé a gauche ou a droite
            if posX == 9 and grid[posX - 1][posY - deplacement] == 0: # check en haut a droite
                if [posX - 1, posY - deplacement] in self.highlighted:
                    return False
                toret.append([posX - 1, posY - deplacement])
            elif posX == 0 and grid[posX + 1][posY - deplacement] == 0: # check en haut a gauche
                if [posX + 1, posY - deplacement] in self.highlighted:
                    return False
                toret.append([posX + 1, posY - deplacement])
            if posX == 9 and grid[posX - 1][posY - deplacement] == other_team and grid[posX - 2][posY - 2 * deplacement] == 0: # check en haut a gauche si il y a un pion et si c'est vide derriere
                if str((posX - 2,posY - 2 * deplacement)) not in self.canEat.keys():
                    self.canEat[str((posX - 2,posY - 2 * deplacement))] = [(posX - 1,posY - deplacement)]
                else:
                    self.canEat[str((posX - 2,posY - 2 * deplacement))].append((posX - 1,posY - deplacement))
                toret.append([posX - 2, posY - 2 * deplacement])

            if posX == 9 and grid[posX - 1][posY + deplacement] == other_team and grid[posX - 2][posY + 2 * deplacement] == 0: # check en bas a gauche si il y a un pion et si c'est vide derriere

                if  str((posX - 2,posY + 2 * deplacement)) not in self.canEat.keys():
                    self.canEat[str((posX - 2, posY + 2 * deplacement))] = [(posX - 1,posY + deplacement)]
                else:
                    self.canEat[str((posX - 2, posY + 2 * deplacement))].append((posX - 1,posY + deplacement))
                toret.append([posX - 2, posY + 2 * deplacement])

            if posX == 0 and grid[posX + 1][posY - deplacement] == other_team and grid[posX + 2][posY - 2 * deplacement] == 0: # check en haut a droite si il y a un pion et si c'est vide derriere

                if  str((posX + 2,posY - 2 * deplacement)) not in self.canEat.keys():
                    self.canEat[str((posX + 2,posY - 2 * deplacement))] = [(posX + 1,posY - deplacement)]
                else:
                    self.canEat[str((posX + 2,posY - 2 * deplacement))].append((posX + 1,posY - deplacement))
                toret.append([posX + 2, posY - 2 * deplacement])

            if posX == 0 and grid[posX + 1][posY + deplacement] == other_team and grid[posX + 2][posY + 2 * deplacement] == 0: # check en bas a droite si il y a un pion et si c'est vide derriere

                if  str((posX + 2,posY + 2 * deplacement)) not in self.canEat.keys():
                    self.canEat[str((posX + 2,posY + 2 * deplacement))] = [(posX + 1,posY + deplacement)]
                else:
                    self.canEat[str((posX + 2,posY + 2 * deplacement))].append((posX + 1,posY + deplacement))
                toret.append([posX + 2, posY + 2 * deplacement])
            if len(self.canEat) != 0:
                recur = self.canPlayRecursively(posX, posY, self.canEat.keys())
                toret.extend(recur)
            return toret

    def tryPlay(self, posX, posY,isVirtual=False):
        """Essaie de jouer a la position posX,posY dans la grille de jeu
                @:parameter posX: Position X dans la grille de jeu
                @:parameter posY: Position Y dans la grille de jeu
                @return: True si le pion a bougé
                @return: False sinon
                """
        if self.selectedPion == None:
            return False
        if [posX, posY] in self.highlighted: #le bout de code suivant sert a jouer le coup

            if str((posX, posY)) in self.canEat.keys():
                key=str((posX, posY))
                print(self.canEat)
                for i in self.canEat[str((posX, posY))]:
                        self.game.grid[i[0]][i[1]]=0
                        self.cases[i[0]][i[1]] = None
            #print(self.canEat)
            self.cases[posX][posY] = self.selectedPion
            self.game.grid[posX][posY] = self.selectedPion.team
            self.game.grid[self.selectedPionPosition[0]][self.selectedPionPosition[1]] = 0
            self.refreshGrid()
            self.highlighted = []
            self.canEat = {}
            self.game.changePlayer()

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
