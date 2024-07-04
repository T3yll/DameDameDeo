import tkinter as tk

class Pion:
    def __init__(self, canvas, x, y, x2, y2, color, team,size=10,isDame=False):
        self.canvas = canvas
        self.team = team
        self.x1 = x
        self.x2 = x2
        self.y1 = y
        self.y2 = y2
        self.color = color
        self.size:float = size
        self.oval = None
        self.isDame = isDame
        self.draw()

    def draw(self):
        self.oval = self.canvas.create_oval(self.x1+self.size, self.y1+self.size, self.x2-self.size, self.y2-self.size, fill=self.color, outline="black")
        if (self.isDame):self.canvas.create_oval(self.x1+self.size+5, self.y1+self.size+5, self.x2-self.size-5, self.y2-self.size-5, outline="red")

    def move_to(self, x, y,x2,y2):
        self.canvas.move(self.oval, x, y)
        self.canvas.tag_raise(self.oval)
        self.x1 = x
        self.y1 = y
        self.x2 = x2
        self.y2 = y2
        self.canvas.create_oval(self.x1+self.size, self.y1+self.size, self.x2-self.size, self.y2-self.size, fill=self.color, outline="black")

