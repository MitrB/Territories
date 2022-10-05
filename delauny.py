from tkinter import *
from tkinter import ttk
from tkinter import Tk, Canvas, Frame, BOTH
from logging import debug, info
from random import randint
from math_functions import *
from helper import *
from GLOBVAR import *
import logging

logging.basicConfig(level=logging.INFO, filename="debug.log", filemode="w")


class Display(Frame):

    def __init__(self, points, triangles):
        super().__init__()

        self.initUI()

        # draw
        for triangle in triangles:
            self.drawTriangle(triangle)
        for point in points:
            self.drawPoint(point, black)
        self.add_label(points)

    def initUI(self):

        self.master.title("Lines")
        self.pack(fill=BOTH, expand=1)

        self.canvas = Canvas(self)

        self.canvas.pack(fill=BOTH, expand=YES)

    def drawPoint(self, point, color):
        x1, y1 = (point[0] - 4), (point[1] - 4)
        x2, y2 = (point[0] + 4), (point[1] + 4)
        self.canvas.create_oval(x1, y1, x2, y2, fill=color)

    def drawTriangle(self, triangle):
        p1, p2, p3 = triangle[0], triangle[1], triangle[2]
        self.canvas.create_line(p1[0], p1[1], p2[0],
                                p2[1], p3[0], p3[1], p1[0], p1[1], fill=python_green)

    def add_label(self, points):
        for point in points:
            self.canvas.create_text(point[0], point[1]+15, text="(%s,%s)" % (
                point[0], point[1]), fill="red", font=('Helvetica 10 bold'))


def main():

    root = Tk()

    # calculate 
    # N = randint(4, 10)
    # points = generate_points(5)
    points = [[522, 743], [280, 612], [1018, 221], [729, 190], [702, 155]]
    info(points)
    hull = convex(points)
    triangles = calculate_pbp_triangulation(points)
    info(triangles)
    info(calculate_triangle_pairs(triangles))
    triangles = calculate_delaunay(triangles)

    display = Display(points, triangles)
    w = str(window_width)
    h = str(window_height)
    root.geometry("%sx%s+0+0" % (w, h))
    root.configure(bg="white")
    root.mainloop()


if __name__ == '__main__':
    main()
