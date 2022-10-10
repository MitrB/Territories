import unittest
from helper import *

class TestMakeNRandomPoints(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestMakeNRandomPoints, self).__init__(*args, **kwargs)
        self.N_1 = 10
        self.N_2 = 100
        self.N_3 = 0 
        self.points_1 = generate_points(self.N_1)
        self.points_2 = generate_points(self.N_2)
        self.points_3 = generate_points(self.N_3)


    def test_amount_of_points(self):
        self.assertEqual(len(self.points_1), self.N_1)
        self.assertEqual(len(self.points_2), self.N_2)
        self.assertEqual(len(self.points_3), self.N_3)

    def test_correct_format(self):
        for point in self.points_1:
            self.assertEqual(type((1,2)), type(point))
            self.assertEqual(type(1), type(point[0]))
            self.assertEqual(type(1), type(point[1]))

if __name__ == '__main__':
    unittest.main()