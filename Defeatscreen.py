import tkinter as tk
import GameBoard

class DefeatScreen:
    def __init__(self):
        self.window = tk.Tk()
        self.window.configure(bg="red", width=800, height=800)
        self.label = tk.Label(self.window, text="Defeat !", font=("Arial", 16), bg="red", fg="white")
        self.label.pack(pady=20)
        
        self.new_game_button = tk.Button(self.window, text="Nouvelle Partie")
        self.new_game_button.pack(pady=10)
        self.quit_button = tk.Button(self.window, text="Quitter")
        self.quit_button.pack(pady=10)
        
    def new_game(self):
        self.window.destroy()
        GameBoard.GameBoard()