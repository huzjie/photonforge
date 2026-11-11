# -*- coding: utf-8 -*-
import unittest

from photonforge.edit import mask, blend, instruct, inpaint, outpaint
from photonforge.flux.base import MockVelocity


class TestMask(unittest.TestCase):
    def test_from_points(self):
        m = mask.from_points(8, 8, [(4, 4)])
        self.assertAlmostEqual(m[4][4], 1.0)

    def test_blur(self):
        m = mask.from_points(16, 16, [(8, 8)], radius=3)
        mb = mask.blur(m, 2)
        self.assertEqual(len(mb), 16)

    def test_invert(self):
        m = mask.from_points(4, 4, [(2, 2)], radius=1)
        mi = mask.invert(m)
        self.assertAlmostEqual(mi[0][0], 1.0)


class TestBlend(unittest.TestCase):
    def test_feather(self):
        base = [[[0.0] * 4 for _ in range(4)] for _ in range(3)]
        m = mask.from_points(4, 4, [(2, 2)])
        out = blend.feather_blend(base, base, m)
        self.assertEqual(len(out[0]), 4)


class TestEdit(unittest.TestCase):
    def test_instruct(self):
        img = [[[0.5] * 8 for _ in range(8)] for _ in range(3)]
        vf = MockVelocity([[[0.9] * 8 for _ in range(8)] for _ in range(3)])
        out = instruct.apply_instruction(img, "把背景换成雪地", vf, "雪地", 0.5)
        self.assertEqual(len(out[0]), 8)

    def test_inpaint(self):
        img = [[[0.5] * 8 for _ in range(8)] for _ in range(3)]
        m = mask.from_points(8, 8, [(4, 4)])
        vf = MockVelocity([[[0.9] * 8 for _ in range(8)] for _ in range(3)])
        out = inpaint.inpaint(img, m, vf, "修复", mask_blur=1)
        self.assertEqual(len(out[0]), 8)

    def test_outpaint(self):
        img = [[[0.5] * 8 for _ in range(8)] for _ in range(3)]
        vf = MockVelocity([[[0.9] * 8 for _ in range(8)] for _ in range(3)])
        out = outpaint.outpaint(img, 2, vf, "扩展")
        self.assertEqual(len(out[0]), 12)


if __name__ == "__main__":
    unittest.main()
