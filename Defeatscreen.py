import tkinter as tk

class DefeatScreen:
    def __init__(self):
        self.window = tk.Tk()
        self.canvas = tk.Canvas(self.window, width=800, height=800)
        self.canvas.pack()
        self.canvas.configure(bg="red")
        self.label = tk.Label(self.canvas, text="Defeat !", font=("Arial", 16), bg="red", fg="white")
        self.label.pack(pady=20)
        
        self.new_game_button = tk.Button(self.canvas, text="Nouvelle Partie")
        self.new_game_button.pack(pady=10)
        self.quit_button = tk.Button(self.canvas, text="Quitter")
        self.quit_button.pack(pady=10)
