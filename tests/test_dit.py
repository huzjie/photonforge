# -*- coding: utf-8 -*-
import unittest

from photonforge.dit import patchify, adaln, attention, rope, mlp, block


class TestPatchify(unittest.TestCase):
    def test_roundtrip(self):
        img = [[[float(x + y) for x in range(4)] for y in range(4)] for _ in range(3)]
        tokens = patchify.patchify(img, patch_size=2)
        out = patchify.unpatchify(tokens, 3, 4, 4, patch_size=2)
        self.assertEqual(len(out), 3)
        self.assertEqual(len(out[0]), 4)


class TestAdaLN(unittest.TestCase):
    def test_modulate_shape(self):
        scale, shift = adaln.modulate([0.1] * 8, 16)
        self.assertEqual(len(scale), 16)
        self.assertEqual(len(shift), 16)

    def test_norm_unit(self):
        x = [1.0, 2.0, 3.0]
        scale = [1.0, 1.0, 1.0]
        shift = [0.0, 0.0, 0.0]
        y = adaln.adaln_norm(x, scale, shift)
        self.assertAlmostEqual(sum(y), 0.0, places=4)


class TestAttention(unittest.TestCase):
    def test_shape(self):
        x = [[0.1] * 8 for _ in range(4)]
        out = attention.attention(x, x, x, num_heads=2)
        self.assertEqual(len(out), 4)
        self.assertEqual(len(out[0]), 8)


class TestRoPE(unittest.TestCase):
    def test_norm_preserved(self):
        x = [3.0, 4.0, 0.0, 0.0]
        y = rope.apply_rope(x, 0)
        self.assertAlmostEqual(y[0] ** 2 + y[1] ** 2, 25.0, places=4)


class TestBlock(unittest.TestCase):
    def test_shape(self):
        x = [[0.1] * 8 for _ in range(3)]
        out = block.dit_block(x, [0.1] * 8, num_heads=2)
        self.assertEqual(len(out), 3)
        self.assertEqual(len(out[0]), 8)


if __name__ == "__main__":
    unittest.main()
