# -*- coding: utf-8 -*-
import unittest

from photonforge.controlnet import canny, depth, pose


class TestControlNet(unittest.TestCase):
    def test_canny(self):
        img = [[[0.0] * 16 for _ in range(16)] for _ in range(3)]
        edges = canny.extract(img)
        self.assertEqual(len(edges), 16)

    def test_depth(self):
        img = [[[0.5] * 8 for _ in range(8)] for _ in range(3)]
        d = depth.estimate(img)
        self.assertEqual(len(d), 8)

    def test_pose(self):
        img = [[[0.5] * 16 for _ in range(16)] for _ in range(3)]
        pts = pose.extract(img)
        self.assertEqual(len(pts), 49)


if __name__ == "__main__":
    unittest.main()
