import tkinter as tk
import pandas as pd
import ia as ia
import game
import Pion
import os

class GameBoard:
    def __init__(self):
        self.window = tk.Tk()
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.canvas = tk.Canvas(self.window, width=800, height=800)
        self.cases = [[None for i in range(10)] for j in range(10)]
        self.game = game.Game()
        self.canvas.grid(row=1, column=1, padx=20, pady=20)
        self.canvas.bind("<Button-1>", self.selectPion)
        self.highlighted = []
        self.selectedPion = None
        self.selectedPionPosition = []
        self.square = 80
        self.allMoves = []
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

        # rafraichit l'affichage de la grille pour update la position des pions
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
        self.print()
        posToPlay = ia.evalMoves(self)
        
        

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
        """Permet de supprimer les carre bleus qui apparaissent lorsqu'on clique sur un pion"""
        for i in self.highlighted:
            self.canvas.create_rectangle(i[0] * 80, i[1] * 80, i[0] * 80 + 80, i[1] * 80 + 80, fill="brown")
        self.highlighted = []

    def isPlayable(self, posX, posY):
        """verifie si une piece a la position posX and posY peut jouer
         et renvoie une liste des coups disponibles ou false si la piece est deja selectionnee"""
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
                @return: True si le pion a bouge
                @return: False sinon
                """
        print("ici")
        if self.selectedPion == None:
            print("TG")
            return False
        if [posX, posY] in self.highlighted: #nouvelle
            self.cases[posX][posY] = self.selectedPion #ancienne pos
            self.allMoves.append(f'{self.selectedPionPosition} -> {[posX, posY]}')


            self.game.grid[posX][posY] = 2
            self.game.grid[self.selectedPionPosition[0]][self.selectedPionPosition[1]] = 0
            print("deplace")
            self.refreshGrid()
            self.highlighted = []
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

if __name__ == '__main__':
    game = GameBoard()
    game.window.mainloop()
    game.export_to_csv()

