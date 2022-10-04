from tkinter import *
from tkinter import ttk
from tkinter import Tk, Canvas, Frame, BOTH
from logging import debug, info
import logging
from math_functions import *
from helper import *

logging.basicConfig(level=logging.INFO, filename="debug.log", filemode="w")


class Display(Frame):

    def __init__(self):
        super().__init__()

        self.initUI()
        points = generate_points()
        for point in points:
            self.drawPoint(point, black)
        self.add_label(points)
        hull = convex(points)
        # for point in hull:
        #     self.drawPoint(point, green)
        triangles = calculate_pbp_triangulation(points)
        info(triangles)
        info(calculate_triangle_pairs(triangles))
        for triangle in triangles:
            self.drawTriangle(triangle)
        # calculate_delaunay(triangles)

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
                                p2[1], p3[0], p3[1], p1[0], p1[1])

    def add_label(self, points):
        for point in points:
            self.canvas.create_text(point[0], point[1]+15, text="(%s,%s)" % (
                point[0], point[1]), fill="black", font=('Helvetica 10 bold'))


def main():

    root = Tk()
    display = Display()
    w = str(window_width)
    h = str(window_height)
    root.geometry("%sx%s+0+0" % (w, h))
    root.mainloop()


if __name__ == '__main__':
    main()
