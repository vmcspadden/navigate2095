import unittest
import numpy as np
from src.navigate.tools.sdf import sphere, box, ellipsoid

class TestSphere(unittest.TestCase):

    def test_sphere_center(self):
        p = np.array([[0], [0], [0]])
        R = 1
        result = sphere(p, R)
        expected = -1
        self.assertEqual(result, expected)

    def test_sphere_surface(self):
        p = np.array([[1], [0], [0]])
        R = 1
        result = sphere(p, R)
        expected = 0
        self.assertEqual(result, expected)

    def test_sphere_outside(self):
        p = np.array([[2], [0], [0]])
        R = 1
        result = sphere(p, R)
        expected = 1
        self.assertEqual(result, expected)

    def test_sphere_inside(self):
        p = np.array([[0.5], [0], [0]])
        R = 1
        result = sphere(p, R)
        expected = -0.5
        self.assertEqual(result, expected)


class TestBox(unittest.TestCase):

    def test_box_center(self):
        p = np.array([[0], [0], [0]])
        w = (1, 1, 1)
        result = box(p, w)
        expected = -1
        self.assertEqual(result, expected)

    def test_box_surface(self):
        p = np.array([[1], [0], [0]])
        w = (1, 1, 1)
        result = box(p, w)
        expected = 0
        self.assertEqual(result, expected)

    def test_box_outside(self):
        p = np.array([[2], [0], [0]])
        w = (1, 1, 1)
        result = box(p, w)
        expected = 1
        self.assertEqual(result, expected)

    def test_box_inside(self):
        p = np.array([[0.5], [0], [0]])
        w = (1, 1, 1)
        result = box(p, w)
        expected = -0.5
        self.assertEqual(result, expected)


class TestEllipsoid(unittest.TestCase):

    def test_ellipsoid_surface(self):
        p = np.array([[1], [0], [0]])
        r = (1, 1, 1)
        result = ellipsoid(p, r)
        expected = 0
        self.assertEqual(result, expected)

    def test_ellipsoid_outside(self):
        p = np.array([[2], [0], [0]])
        r = (1, 1, 1)
        result = ellipsoid(p, r)
        expected = 1
        self.assertEqual(result, expected)

    def test_ellipsoid_inside(self):
        p = np.array([[0.5], [0], [0]])
        r = (1, 1, 1)
        result = ellipsoid(p, r)
        expected = -0.5
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()