from tkinter import *
from logging import debug, info
from random import randint, choice
from src.math_functions.math_functions import *
from src.math_functions.precalc import *


class Display(Frame):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.master.title("Lines")
        self.pack(fill=BOTH, expand=1)

        self.canvas = Canvas(self)
        self.canvas.pack(fill=BOTH, expand=YES)

    def drawPoint(self, point, color):
        x1, y1 = (point[0] - 4), (point[1] - 4)
        x2, y2 = (point[0] + 4), (point[1] + 4)
        self.canvas.create_oval(x1, y1, x2, y2, fill=color)

    def drawTriangle(self, triangle, color="R"):
        p1, p2, p3 = triangle[0], triangle[1], triangle[2]
        if color == "R":
            color = "#"+''.join([choice('0123456789ABCDEF') for j in range(6)])

        self.canvas.create_polygon(
            p1[0], p1[1], p2[0], p2[1], p3[0], p3[1], fill=color)

    def drawTriangleOutline(self, triangle):
        p1, p2, p3 = triangle[0], triangle[1], triangle[2]
        self.canvas.create_line(p1[0], p1[1], p2[0],
                                p2[1], p3[0], p3[1], p1[0], p1[1], fill="black")

    def add_label(self, points):
        for point in points:
            self.canvas.create_text(point[0], point[1]+15, text="(%s,%s)" % (
                point[0], point[1]), fill="black", font=('Helvetica 10 bold'))


def setup_tk():
    # Setup Tk
    root = Tk()
    display = Display()
    w = str(window_width)
    h = str(window_height)
    root.geometry("%sx%s+0+0" % (w, h))
    root.configure(bg="white")

    return (root, display)

def start_tk_loop(root):
    root.mainloop()

def main():
    # Get delauny
    (points, triangles) = delaunay_request()

    (root, display) = setup_tk()

    # Draw
    for triangle in triangles:
        display.drawTriangle(triangle)
        display.drawTriangleOutline(triangle)
    for point in points:
        display.drawPoint(point, black)
    display.add_label(points)

    start_tk_loop(root)


def draw_territories(display, map):
    for triangle in map.polygons.keys():
        display.drawTriangle(triangle.shape, triangle.color)

if __name__ == '__main__':
    main()
