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


    # calculate 
    N = randint(10, 500)
    points = generate_points(N)
    # points = [[1283, 682], [1252, 800], [1238, 739], [1825, 592], [1464, 848], [162, 575], [278, 641], [1780, 220], [1086, 861], [760, 21], [581, 424], [671, 398], [1117, 876], [1286, 648], [1455, 985], [284, 384], [16, 824], [1369, 110], [1414, 506], [738, 930], [1101, 227], [1251, 141], [943, 660], [792, 753], [209, 137], [11, 1069], [952, 430], [1328, 202], [1051, 871], [1635, 469], [1462, 262], [70, 376], [547, 714], [1080, 91], [1616, 809], [114, 977], [1829, 634], [421, 962], [1439, 575], [352, 550], [956, 576], [1423, 74], [1137, 917], [1757, 323], [467, 30], [1718, 996], [1279, 508], [1832, 134], [611, 297], [1465, 720], [838, 158], [998, 437], [1795, 977], [1190, 522], [542, 169], [939, 817], [324, 764], [91, 58], [281, 498], [414, 230], [538, 634], [1750, 214], [144, 912], [1691, 300], [1207, 479], [535, 476], [253, 120], [1151, 415], [340, 966], [333, 926], [1274, 702], [394, 877], [1206, 558], [1701, 510], [411, 503], [1460, 11], [847, 863], [342, 642], [171, 419], [623, 616], [581, 31], [1030, 486], [356, 56], [1141, 328], [481, 948], [1707, 1035], [590, 978], [607, 359], [1350, 345], [1400, 292], [1578, 532], [1784, 7], [24, 6], [1609, 351], [1804, 850], [1774, 901], [91, 456], [1454, 82], [1576, 542], [1701, 417], [735, 121], [1289, 187], [929, 710], [82, 818], [1116, 240], [508, 408], [1773, 597], [948, 823], [236, 894], [1731, 691], [1370, 329], [562, 427], [857, 939], [1610, 295], [942, 990], [1430, 589], [424, 551], [414, 545], [332, 874], [1457, 133], [1067, 524], [1304, 315], [96, 519], [1077, 1062], [810, 125], [1852, 960], [1252, 626], [104, 291], [350, 158], [1138, 1022], [1845, 834], [1505, 837], [540, 1018], [1392, 833], [171, 910], [1361, 421], [1833, 575], [1365, 551], [1001, 603], [974, 627], [412, 1011], [202, 882], [621, 996], [471, 836], [11, 905], [510, 665], [895, 195], [663, 407], [193, 286], [1651, 686], [635, 580], [1084, 308], [709, 895], [1542, 128], [1105, 375], [1541, 207], [1073, 157], [1365, 293], [304, 713], [1264, 351], [492, 69], [11, 594], [1514, 566], [899, 781], [109, 804], [448, 684], [230, 912], [747, 886], [1327, 906], [205, 891], [749, 780], [720, 739], [699, 280], [1341, 877], [86, 867], [165, 323], [1757, 586], [1246, 386], [818, 232], [1245, 84], [766, 463], [1435, 161], [156, 695], [1512, 684], [1871, 350], [1009, 341], [146, 770], [593, 739], [1159, 682], [1330, 1009], [1707, 79], [1754, 1062], [902, 68], [737, 663], [1118, 216], [1707, 397], [196, 991], [944, 565], [1098, 907], [87, 339], [1802, 700], [73, 278], [277, 265], [274, 25], [967, 545], [505, 296], [129, 915]]
    info(points)
    hull = convex(points)
    triangles = calculate_pbp_triangulation(points)
    info(triangles)
    triangles = calculate_delaunay(triangles)
    info(triangles)


    # Tk
    root = Tk()
    display = Display(points, triangles)
    w = str(window_width)
    h = str(window_height)
    root.geometry("%sx%s+0+0" % (w, h))
    root.configure(bg="white")
    root.mainloop()


if __name__ == '__main__':
    main()
