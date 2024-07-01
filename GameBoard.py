import tkinter as tk
import pandas as pd
import ia as ia
import game as G
import Pion
import os

class GameBoard:
    def __init__(self,isVirtual=False):
        if isVirtual==False:
            self.window = tk.Tk()
            self.canvas = tk.Canvas(self.window, width=800, height=800)
            self.canvas.grid(row=1, column=1, padx=20, pady=20)
            self.canvas.bind("<Button-1>", self.selectPion)
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.cases = [[None for i in range(10)] for j in range(10)]
        self.game = G.Game()
        self.allMoves = []
        self.highlighted = []  #positions des cases mise en bleu a la selection d'un pion [[x,y],[x2,y2],...]
        self.canEat = {} #dictionnaire avec pour clé la position d'arrivee sous forme de string '(x,y)' et pour valeurs la position du pion mangé lors du deplacement
        self.canEatRec={} #dictionnaire avec pour clé la position d'arrivee sous forme de string '(x,y)' et pour valeurs les positions des pions mangés lors du deplacement
        self.selectedPion = None #Objet Pion de la case selectionnée
        self.selectedPionPosition = [] #Position du Pion de la case selectionnée
        self.square = 80 #Taille des carrés
        self.Dames=[]
        self.path= []
        if isVirtual == False:
            self.refreshGrid()

       # print(self.cases)



    def getParcour(self,arrivee,dame=False):
        todelete=[]
        if arrivee not in self.path:
            return todelete
        if dame==False:
            for i in range(len(self.path)-1):
                if self.path[i]==arrivee:
                    return todelete
                tmp=(int(abs(self.path[i][0]+self.path[i+1][0])/2),int((abs(self.path[i][1]+self.path[i+1][1])/2)))
                todelete.append(tmp)
        else:
            pass



        return todelete




    def checkCoup(self,x,y,deplacement,dame=False):

        toret=[]
        if dame == False:
            for i,j in enumerate([[x+1,y-deplacement],[x-1,y-deplacement]]):
                try:
                    if self.game.grid[j[0]][j[1]] == 0:
                        toret.append(j)
                except IndexError as e:
                    print(e)
                    continue
            return toret
        else:
            pas=1
            tocheck = [[1, - 1],
                       [ - 1, - 1],
                       [  1, 1],
                       [ - 1, 1]]
            for j in tocheck:
                pas=1
                while pas<10:
                    try:
                        if self.game.grid[x+j[0]*pas][y+j[1]*pas]==0:
                            toret.append([x+j[0]*pas,y+j[1]*pas])
                        else:
                            break

                        pas += 1
                    except IndexError as e:
                        pas += 1
                        continue

            return toret



    def checkCoupsRec(self,x,y,teamtocheck,toret=[],checkedalready=[],depart=(),dame=False,currentDirection=None):
        if [x, y] in checkedalready:
            return toret

        if dame==False:
            if [x,y] in checkedalready:
                return toret
            forward=[x + 2, y + 2], [x - 2, y + 2], [x + 2, y - 2], [x - 2, y - 2]
            for i,j in enumerate([[x+1,y+1],[x-1,y+1],[x+1,y-1],[x-1,y-1]]):
                try:

                    if self.game.grid[j[0]][j[1]] == teamtocheck and self.game.grid[forward[i][0]][forward[i][1]] == 0:
                        toret.append(forward[i])
                        self.canEatRec.setdefault(str((forward[i][0], forward[i][1])), [])
                        if str((forward[i][0], forward[i][1])) in self.canEatRec.keys():
                            self.canEatRec[str((forward[i][0], forward[i][1]))].append([j[0], j[1]])
                        else:
                            self.canEatRec[str((forward[i][0], forward[i][1]))] = [[j[0], j[1]]]
                        checkedalready.append([x, y])
                        return self.checkCoupsRec(forward[i][0], forward[i][1], teamtocheck, toret,
                                                  checkedalready=checkedalready, depart=depart)
                except IndexError as e:
                    print(e)
                    continue
            return toret
        else:
            print("passage recursif",x,y)
            pas = 1

            tocheck = [[1, - 1],[- 1, - 1],[1, 1],[- 1, 1]]
            for j in tocheck:
                print(j)
                pas = 1
                while pas < 10:
                    try:
                        if self.game.grid[x + j[0] * pas][y + j[1] * pas] == teamtocheck and self.game.grid[x + j[0] * (pas+1)][y + j[1] * (pas+1)] == 0:
                            toret.append([x + j[0] * (pas+1), y + j[1] * (pas+1)])
                            checkedalready.append([x, y])
                            self.checkCoupsRec(x + j[0] * (pas+1), y + j[1] * (pas+1),teamtocheck,toret,checkedalready,dame=True,currentDirection=j)
                        elif self.game.grid[x + j[0] * pas][y + j[1] * pas] == 0:
                            if currentDirection!=None:
                                if j==currentDirection:
                                    toret.append([x + j[0] * pas, y + j[1] * pas])
                                    pas += 1
                                    continue
                            else:
                                toret.append([x + j[0] * pas, y + j[1] * pas])
                                pas += 1
                                continue
                        else:
                            pas=10
                        pas += 1
                    except IndexError as e:
                        pas += 1
                        continue

            return toret








    def refreshGrid(self):

        """rafraichit l'affichage de la grille pour update la position des pions"""
        self.canvas.delete("all")

        for i, j in enumerate(self.game.grid):
            for k, l in enumerate(j):

                isDame =  True if [i,k] in self.Dames else False

                color = "brown" if (i + k) % 2 == 0 else "grey"
                self.canvas.create_rectangle(i * self.square, k * self.square, i * self.square + self.square,
                                             k * self.square + self.square, fill=color)
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
                self.canvas.create_text(i * self.square+10, k * self.square+30, fill="yellow", text=str((i, k)), width=10,justify="center",anchor="center")

    def selectPion(self, event):
        """selectione un pion sur le plateau"""
        #self.print()
        for x, row in enumerate(self.cases):
            for y, cell in enumerate(row):
                if cell == None and [x, y] in self.highlighted and (event.x > x * self.square and event.x < (x + 1) * self.square) and (event.y > y * self.square and event.y < (y + 1) * self.square):
                    self.tryPlay(x, y)
                if cell != None and (event.x > cell.x1 and event.x < cell.x2) and (event.y > cell.y1 and event.y < cell.y2) and cell.team == self.game.current:
                    if cell.isDame==True:
                        posToPlay = self.isPlayableDame(x, y)
                    else:
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

    def isPlayableDame(self, posX, posY):
        """verifie si une dame a la position posX and posY peut jouer
         et renvoie une liste des coups disponibles ou false si la piece est deja selectionnéé"""
        #print(int(posX))
        grid = self.game.grid
        cases = self.cases
        self.deleteHighlighted()
        self.selectedPion = cases[posX][posY]
        self.selectedPionPosition = [posX, posY]
        deplacement= -1 if (self.selectedPion.team==1) else 1
        toret = []
        other_team = 2 if (self.selectedPion.team==1) else 1
        tocheck = 0 if (self.selectedPion.team==1) else 9
        toret=self.checkCoup(posX, posY, deplacement,dame=True)
        self.path = [[posX, posY]]
        self.path.extend(self.checkCoupsRec(posX, posY, other_team, toret=[], depart=(posX, posY), checkedalready=[],dame=True))
        toret.extend(self.path[1:])
        #self.path = [[posX, posY]]
        #self.path.extend(self.checkCoupsRec(posX, posY, other_team, toret=[], depart=(posX, posY), checkedalready=[]))
        #toret.extend(self.path[1:])
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
        deplacement= -1 if (self.selectedPion.team==1) else 1
        toret = []
        other_team = 2 if (self.selectedPion.team==1) else 1
        tocheck = 0 if (self.selectedPion.team==1) else 9
        toret=self.checkCoup(posX, posY, deplacement)
        self.path = [[posX, posY]]
        self.path.extend(self.checkCoupsRec(posX, posY, other_team, toret=[], depart=(posX, posY), checkedalready=[]))
        toret.extend(self.path[1:])
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
            for i in self.getParcour([posX,posY]):
                self.game.grid[i[0]][i[1]] = 0

            # if str((posX, posY)) in self.canEat.keys():
            #     key = str((posX, posY))
            #     print(self.canEat)
            #     toeat = self.canEat[key]
            #     print(toeat)
            #     self.game.grid[toeat[0]][toeat[1]]=0
            #print(self.canEat)
            self.allMoves.append(f'{self.selectedPionPosition} -> {[posX, posY]}')
            if self.selectedPionPosition in self.Dames:
                self.Dames.remove(self.selectedPionPosition)
                self.Dames.append([posX, posY])

            self.cases[posX][posY] = None
            self.cases[posX][posY] = self.selectedPion
            self.game.grid[posX][posY] = self.selectedPion.team
            self.game.grid[self.selectedPionPosition[0]][self.selectedPionPosition[1]] = 0
            tocheck = 9 if (self.selectedPion.team == 1) else 0
            print(tocheck,posY)
            if posY == tocheck and [posX, posY] not in self.Dames:
                print("connard")
                self.Dames.append([posX, posY])
            self.refreshGrid()
            self.highlighted = []
            self.canEat = {}
            self.canEatRec={}

            if not self.game.changePlayer():
                #victoire
                pass



            if not self.game.isEnd() == False:
                print("finito")
            return True

    def export_to_csv(self):
        filename = 'moves1.csv'
        if os.path.exists(filename):
            df = pd.read_csv(filename, index_col=0)
        else:
            df = pd.DataFrame()
        game_number = 1
        col_name = f'game{game_number}'
        if col_name not in df.columns:
            df[col_name] = ''
        white_move_number = 1
        black_move_number = 1
        for i in range(len(self.allMoves)):
            if i % 2 == 0:
                line_name = f'white{white_move_number}'
                white_move_number += 1
            else:
                line_name = f'black{black_move_number}'
                black_move_number += 1
            df.at[line_name, col_name] = self.allMoves[i]
        df.to_csv(filename, index_label='Index')

    def on_closing(self):
        self.export_to_csv()
        self.window.destroy()

    def get_all_pieces_positions(self):
        """retourne la liste des pions"""
        pieces_positions = [] #changer ca en dico
        for x, row in enumerate(self.cases):
            for y, cell in enumerate(row):
                if cell is not None:
                    pieces_positions.append({"position": (x, y), "color": cell.team})
        return pieces_positions

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
    game.export_to_csv()

