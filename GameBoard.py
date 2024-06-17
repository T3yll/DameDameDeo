import tkinter as tk

class GameBoard:
    def __init__(self):
        self.window = tk.Tk()
        self.buttons = [[None for _ in range(10)] for _ in range(10)]

        for i in range(10):
            for j in range(10):
                color = "brown" if (i + j) % 2 == 0 else "grey"
                self.buttons[i][j] = tk.Button(
                    self.window,
                    text=" ",
                    font=("Arial", 20),
                    width=3,
                    height=1,
                    bg=color,
                    command=lambda row=i, col=j: self.on_button_click(row, col)
                )
                self.buttons[i][j].grid(row=i, column=j)

    def on_button_click(self, row, col):
        
        pass

game = GameBoard()
game.window.mainloop()