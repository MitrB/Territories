from tkinter import *
from logging import debug, info
from random import randint, choice
from math_functions.math_functions import *
from src.math_functions.precalc import *
import logging

logging.basicConfig(level=logging.INFO, filename="debug.log", filemode="w")

# disable/enable logging
logging.disable(logging.DEBUG)
# logging.disable(logging.INFO)


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

    return (display, root)


def main():
    # Get delauny
    (points, triangles) = delaunay_request()

    (display, root) = setup_tk()

    # Draw
    for triangle in triangles:
        display.drawTriangle(triangle)
        display.drawTriangleOutline(triangle)
    for point in points:
        display.drawPoint(point, black)
    display.add_label(points)

    root.mainloop()


def draw_territories(map, points):
    (display, root) = setup_tk()

    for triangle in map.polygons.keys():
        display.drawTriangle(triangle.shape, "R")
    
    for point in points:
        display.drawPoint(point, black)
    display.add_label(points)

    root.mainloop()


if __name__ == '__main__':
    main()
