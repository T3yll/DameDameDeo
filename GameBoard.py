import tkinter as tk
import generationDico as gd

import game
import Pion
class GameBoard:
    def __init__(self):
        self.window = tk.Tk()
        self.canvas = tk.Canvas(self.window, width=800, height=800)
        self.cases = [[tk.Frame for _ in range(10)] for _ in range(10)]
        self.game = game.Game()
        self.canvas.grid(row=1, column=1, padx=20, pady=20)
        square=80
        for i,j in enumerate(self.game.grid):
            for k,l in enumerate(j):
                color = "brown" if (i + k) % 2 == 0 else "grey"
                self.canvas.create_rectangle(i*square,k*square , i*square+square, k*square+square, fill=color)
                if l==1:
                    pion = Pion.Pion(self.canvas,i*square,k*square , i*square+square, k*square+square,"black",5)
                elif l==2:
                    pion = Pion.Pion(self.canvas, i * square, k * square, i * square + square, k * square + square,"white", 5)





    def on_button_click(self, row, col):
        
        pass




if __name__ == '__main__':
    game = GameBoard()
    game.window.mainloop()
