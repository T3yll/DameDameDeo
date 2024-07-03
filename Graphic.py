import tkinter as tk

class Graphic:
    def __init__(self):
        self.window = tk.Tk()
        self.canvas = tk.Canvas(self.window, width=800, height=800)
        self.canvas.pack()
        self.window.title("GRAPHIC")

        self.new_game_button = tk.Button(self.window, text="Nouvelle Partie", command=on_new_game)
        self.new_game_button.pack(pady=10)
        self.quit_button = tk.Button(self.window, text="Quitter", command=on_quit)
        self.quit_button.pack(pady=10)