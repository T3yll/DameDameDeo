import tkinter as tk

class Pion:
    def __init__(self, canvas, x, y, color, size=30):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.oval = None
        self.draw()

    def draw(self):
        x1 = self.x - self.size / 2
        y1 = self.y - self.size / 2
        x2 = self.x + self.size / 2
        y2 = self.y + self.size / 2
        self.oval = self.canvas.create_oval(x1, y1, x2, y2, fill=self.color, outline="black")

    def move_to(self, x, y):
        dx = x - self.x
        dy = y - self.y
        self.canvas.move(self.oval, dx, dy)
        self.x = x
        self.y = y