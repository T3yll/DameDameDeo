import tkinter as tk
import GameBoard
import Graphic

class VictoryScreen:
    def __init__(self):
        self.window = tk.Tk()
        self.window.configure(bg="green")
        self.label = tk.Label(self.window, text="Victoire !", font=("Arial", 16), bg="green", fg="white")
        self.label.pack(pady=20)
        
        self.new_game_button = tk.Button(self.window, text="Nouvelle Partie", command=self.new_game)
        self.new_game_button.pack(pady=10)
        self.quit_button = tk.Button(self.window, text="Quitter", command=self.window.quit)
        self.quit_button.pack(pady=10)
        self.new_graphic_button = tk.Button(self.window, text="Graphic", command=self.graphic)
        self.new_graphic_button.pack(pady=10)
        
    def new_game(self):
        self.window.destroy()
        GameBoard.GameBoard()

    def graphic(self):
        csv_file = 'moves1.csv'
        game_graphic = Graphic.Graphic(csv_file)
        game_graphic.run()