from tkinter import *
from tkinter import ttk
from tkinter import Tk, Canvas, Frame, BOTH
from random import randint

window_width = 1000
window_height = 1000
python_green = "#476042"
green = "#000fff000"
black = "#000000"
color2 = "#125233"


# https://lvngd.com/blog/convex-hull-graham-scan-algorithm-python/
def convex(points):
    points = points.copy()
    points.sort(key=lambda x: [x[0], x[1]])
    hull = []
    start = points.pop(0)
    hull.append(start)
    points.sort(key=lambda p: (get_slope(p, start), -p[1], p[0]))
    while points != []:
        hull.append(points.pop(0))
        while len(hull) > 2 and get_cross_product(hull[-3], hull[-2], hull[-1]) < 0:
            hull.pop(-2)
    return hull


def get_slope(p1, p2):
    if p1[0] == p2[0]:
        return float('inf')
    else:
        return 1.0*(p1[1]-p2[1])/(p1[0]-p2[0])


def get_cross_product(p1, p2, p3):
    return ((p2[0] - p1[0])*(p3[1] - p1[1])) - ((p2[1] - p1[1])*(p3[0] - p1[0]))


def calculate_pbp_triangulation(points):
    points.sort(key=lambda x: [x[0], x[1]])
    print("POINTS:")
    print(points)

    triangles = []
    triangles.append(points[:3])
    points_done = points[:3]
    points = points[3:]
    while points != []:
        point = points.pop(0)
        print("DONE:")
        print(points_done)
        convex_shape = convex(points_done)
        convex_shape.append(convex_shape[0])
        print("CONVEX:")
        print(convex_shape)
        for i in range(0, len(convex_shape)-1):
            p1, p2, p3 = convex_shape[i], convex_shape[i+1], point
            print(p1 + p2 + p3)
            if (get_cross_product(p1, p2, p3) < 0):
                triangles.append([p1, p2, p3])
        points_done.append(point)

    print("POINTS DONE:")
    print(points_done)

    return (triangles)


def calculate_delaunay(points):
    pass


class Display(Frame):

    def __init__(self):
        super().__init__()

        self.initUI()
        points = self.generate_points()
        for point in points:
            self.drawPoint(point, black)
        self.add_label(points)
        hull = convex(points)
        # for point in hull:
        #     self.drawPoint(point, green)
        triangles = calculate_pbp_triangulation(points)
        for triangle in triangles:
            self.drawTriangle(triangle)

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

    def generate_points(self):
        # N = randint(0, 100)
        N = 10
        points = [[randint(0, window_width - 10), randint(0, window_height - 10)]
                  for i in range(N)]
        return points

    def add_label(self, points):
        for point in points:
            self.canvas.create_text(point[0], point[1]+15, text="(%s,%s)"%(point[0],point[1]), fill="black", font=('Helvetica 10 bold'))



def main():

    root = Tk()
    display = Display()
    w = str(window_width)
    h = str(window_height)
    root.geometry("%sx%s+0+0" % (w, h))
    root.mainloop()


if __name__ == '__main__':
    main()
