import tkinter as tk
import GameBoard

class Regle:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Règles du Jeu")
        self.window.geometry("900x300")

        self.canvas = tk.Canvas(self.window)
        self.canvas.grid(row=0, column=0, padx=20, pady=20)

        self.button_frame = tk.Frame(self.window)
        self.button_frame.grid(row=0, column=0, padx=20, pady=20, sticky="n")

        self.new_game_button = tk.Button(self.button_frame, text="Nouvelle Partie", command=self.newGame)
        self.new_game_button.pack(pady=10)

        self.quit_button = tk.Button(self.button_frame, text="Quitter", command=self.window.quit)
        self.quit_button.pack(pady=100)

        self.regles_label = tk.Label(self.window, text="Règles du Jeu", font=("Helvetica", 16, "bold"))
        self.regles_label.grid(row=0, column=0, padx=20, pady=10)

        self.regles_texte = (
            "1. Chaque joueur commence avec 12 pions.\n"
            "2. Les pions se déplacent en diagonale vers l'avant, d'une case à la fois, sur les cases foncées.\n"
            "3. Si un pion atteint la dernière rangée de l'adversaire, il est promu en dame.\n"
            "4. Une dame se déplace en diagonale, en avant et en arrière, sur n'importe quel nombre de cases non obstruées.\n"
            "5. Le jeu se termine lorsqu'un joueur ne peut plus effectuer de déplacement légal, soit parce que tous ses pions ont été capturés, soit parce qu'ils sont bloqués."
        )

        self.rules_text = tk.Text(self.window, width=100, height=10, wrap="word")
        self.rules_text.insert(tk.END, self.regles_texte)
        self.rules_text.config(state=tk.DISABLED)
        self.rules_text.grid(row=0, column=0, padx=20, pady=20)

    def newGame(self):
        self.window.destroy()
        GameBoard.GameBoard()

