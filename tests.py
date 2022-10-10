import unittest
from helper import *

class TestMakeNRandomPoints(unittest.TestCase):

    def test_amount_of_points(self):
        N = 10
        points = generate_points(N)
        self.assertEqual(len(points), N)


if __name__ == '__main__':
    unittest.main()