from tkinter import Tk, Canvas
from itertools import product

class Board(Tk):
    def __init__(self, size):
        Tk.__init__(self)
        self.cellsize = size / 7
        self.canvas = Canvas(self, width=size, height=size)
        self.canvas.bind("<Button-1>", self.onclick)
        self.canvas.pack()
    def draw_rectangle(self, x1, y1, x2, y2, color):
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
    def onclick(self, event):
        i = int(event.x / self.cellsize)
        j = int(event.y / self.cellsize)
        x = int(event.x / self.cellsize) * self.cellsize
        y = int(event.y / self.cellsize) * self.cellsize
        self.draw_rectangle(x, y, x + self.cellsize, y + self.cellsize, 'black')
        print ("You clicked on cell (%s, %s)" % (i, j))


size = 400
square_size = size / 7
board = Board(size)
board.title("Isola")

for (i, j) in product(range(7), range(7)):
    coordX1 = (i * square_size)
    coordY1 = (j * square_size)
    coordX2 = coordX1 + square_size
    coordY2 = coordY1 + square_size
    color = "white" #if i%2 == j%2 else "black"
    board.draw_rectangle(coordX1, coordY1, coordX2, coordY2, color)

board.mainloop()
