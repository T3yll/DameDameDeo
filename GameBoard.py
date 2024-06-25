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

        self.highlighted = []  #positions des cases mise en bleu a la selection d'un pion [[x,y],[x2,y2],...]
        self.canEat = {} #dictionnaire avec pour clé la position d'arrivee sous forme de string '(x,y)' et pour valeurs la position du pion mangé lors du deplacement
        self.canEatRec={} #dictionnaire avec pour clé la position d'arrivee sous forme de string '(x,y)' et pour valeurs les positions des pions mangés lors du deplacement
        self.selectedPion = None #Objet Pion de la case selectionnée
        self.selectedPionPosition = [] #Position du Pion de la case selectionnée
        self.square = 80 #Taille des carrés
        self.currDame=()
        if isVirtual == False:
            self.refreshGrid()

       # print(self.cases)



    def checkCoupsRec(self,x,y,teamtocheck,toret=[],checkedalready=[],depart=()):
        print('checkCoupsRec')
        if [x,y] in checkedalready:
            return toret
        forward=[x + 2, y + 2], [x - 2, y + 2], [x + 2, y - 2], [x - 2, y - 2]
        for i,j in enumerate([[x+1,y+1],[x-1,y+1],[x+1,y-1],[x-1,y-1]]):
            try:
                if self.game.grid[j[0]][j[1]] == teamtocheck and self.game.grid[forward[i][0]][forward[i][1]]==0:
                    toret.append(forward[i])
                    checkedalready.append([x,y])
                    self.canEatRec.setdefault(str((forward[i][0],forward[i][1])),[])
                    if str((forward[i][0],forward[i][1])) in self.canEatRec.keys():
                        print("debugDepart = ",str(depart))
                        print("debug = ",self.canEatRec)
                        self.canEatRec[str((forward[i][0],forward[i][1]))].append([j[0],j[1]])
                    else:
                        self.canEatRec[str((forward[i][0],forward[i][1]))]=[[j[0],j[1]]]
                    return self.checkCoupsRec(forward[i][0],forward[i][1],teamtocheck,toret,checkedalready=checkedalready,depart=depart)
            except IndexError as e:
                print(e)
                continue
        return toret







    def refreshGrid(self):

        """rafraichit l'affichage de la grille pour update la position des pions"""
        self.canvas.delete("all")

        for i, j in enumerate(self.game.grid):
            for k, l in enumerate(j):
                isDame=True
                color = "brown" if (i + k) % 2 == 0 else "grey"
                self.canvas.create_rectangle(i * self.square, k * self.square, i * self.square + self.square,
                                             k * self.square + self.square, fill=color)
                if (i,k)==(self.currDame):
                    isDame=True
                if l == 1:
                    pion = Pion.Pion(self.canvas, i * self.square, k * self.square, i * self.square + self.square,
                                     k * self.square + self.square, "black", 1,isDame=isDame)
                    self.cases[i][k] = pion
                elif l == 2:
                    pion = Pion.Pion(self.canvas, i * self.square, k * self.square, i * self.square + self.square,
                                     k * self.square + self.square, "white", 2,isDame=isDame)
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
        self.canEatRec = {}


    def isPlayable(self, posX, posY):
        """verifie si une piece a la position posX and posY peut jouer
         et renvoie une liste des coups disponibles ou false si la piece est deja selectionnéé"""
        #print(int(posX))
        grid = self.game.grid
        cases = self.cases
        self.deleteHighlighted()
        self.selectedPion = cases[posX][posY]
        self.selectedPionPosition = [posX, posY]
        print("canEatRec= ",self.canEatRec)
        deplacement= -1 if (self.selectedPion.team==1) else 1
        toret = []
        other_team = 2 if (self.selectedPion.team==1) else 1
        tocheck = 0 if (self.selectedPion.team==1) else 9



        if not (posX == 0 or posX == 9):


            if (not posX == 0) and grid[posX - 1][posY - deplacement] == other_team and grid[posX - 2][posY - 2 * deplacement] == 0:
                print("passé",1)
                self.canEat[str((posX - 2,posY - 2 * deplacement))]=(posX - 1,posY - deplacement)
                toret.append([posX - 2, posY - 2 * deplacement])
            print("posY= ",posY)
            print("check= ", tocheck)
            if not posY==tocheck and not posX == 0 and grid[posX - 1][posY + deplacement] == other_team and grid[posX - 2][posY + 2 * deplacement] == 0:
                print("passé", 2)
                self.canEat[str((posX - 2, posY + 2 * deplacement))]=(posX - 1, posY + deplacement)
                toret.append([posX - 2, posY + 2 * deplacement])

            if (not posX == 8) and grid[posX + 1][posY - deplacement] == other_team and grid[posX + 2][posY - 2 * deplacement] == 0:
                print("passé", 3)
                self.canEat[str((posX + 2,posY - 2 * deplacement))]=(posX + 1,posY - deplacement)

                toret.append([posX + 2, posY - 2 * deplacement])

            if not posY==tocheck and (not posX == 8) and grid[posX + 1][posY + deplacement] == other_team and grid[posX + 2][posY + 2 * deplacement] == 0:
                self.canEat[str((posX + 2, posY + 2 * deplacement))]=(posX + 1, posY + deplacement)
                print("passé", 4)
                toret.append([posX + 2, posY + 2 * deplacement])
            if grid[posX - 1][posY - deplacement] == 0:
                if [posX - 1, posY - deplacement] in self.highlighted:
                    return False
                toret.append([posX - 1, posY - deplacement])
            if grid[posX + 1][posY - deplacement] == 0:
                if [posX + 1, posY - deplacement] in self.highlighted:
                    return False
                toret.append([posX + 1, posY - deplacement])

            toret.extend(self.checkCoupsRec(posX, posY, other_team,toret=[],depart=(posX, posY),checkedalready=[]))

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
                self.canEat[str((posX - 2,posY - 2 * deplacement))] = (posX - 1,posY - deplacement)

                toret.append([posX - 2, posY - 2 * deplacement])

            if (not posY==tocheck) and posX == 9 and grid[posX - 1][posY + deplacement] == other_team and grid[posX - 2][posY + 2 * deplacement] == 0: # check en bas a gauche si il y a un pion et si c'est vide derriere

                self.canEat[str((posX - 2, posY + 2 * deplacement))] = (posX - 1,posY + deplacement)

                toret.append([posX - 2, posY + 2 * deplacement])

            if not posY==tocheck and posX == 0 and grid[posX + 1][posY - deplacement] == other_team and grid[posX + 2][posY - 2 * deplacement] == 0: # check en haut a droite si il y a un pion et si c'est vide derriere

                self.canEat[str((posX + 2,posY - 2 * deplacement))] = (posX + 1,posY - deplacement)

                toret.append([posX + 2, posY - 2 * deplacement])

            if posX == 0 and grid[posX + 1][posY + deplacement] == other_team and grid[posX + 2][posY + 2 * deplacement] == 0: # check en bas a droite si il y a un pion et si c'est vide derriere

                self.canEat[str((posX + 2,posY + 2 * deplacement))] = (posX + 1,posY + deplacement)

                toret.append([posX + 2, posY + 2 * deplacement])

            return toret

    def tryPlay(self, posX, posY,isVirtual=False):
        """Essaie de jouer a la position posX,posY dans la grille de jeu
                @:parameter posX: Position X dans la grille de jeu
                @:parameter posY: Position Y dans la grille de jeu
                @return: True si le pion a bougé
                @return: False sinon
                """
        print("caneatrec =",self.canEatRec)
        if self.selectedPion == None:
            return False
        if [posX, posY] in self.highlighted: #le bout de code suivant sert a jouer le coup
            print("mange recursif  =>  ", str((posX, posY)))
            if str((posX, posY)) in self.canEatRec.keys():
                for i in self.canEatRec[str((posX, posY))]:

                    self.game.grid[i[0]][i[1]] = 0
            elif str((posX, posY)) in self.canEat.keys():
                key = str((posX, posY))
                print(self.canEat)
                toeat = self.canEat[key]
                print(toeat)
                self.game.grid[toeat[0]][toeat[1]]=0
            #print(self.canEat)
            self.cases[posX][posY] = None
            self.cases[posX][posY] = self.selectedPion
            self.game.grid[posX][posY] = self.selectedPion.team
            self.game.grid[self.selectedPionPosition[0]][self.selectedPionPosition[1]] = 0
            self.refreshGrid()
            self.highlighted = []
            self.canEat = {}
            self.canEatRec={}
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

if __name__ == "__main__":
    game = GameBoard()
    game.window.mainloop()
