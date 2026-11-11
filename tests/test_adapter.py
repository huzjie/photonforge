# -*- coding: utf-8 -*-
import unittest

from photonforge.adapter import reference, cross_attention, weighting, modes


class TestReference(unittest.TestCase):
    def test_encode(self):
        img = [[[0.5 for _ in range(16)] for _ in range(16)] for _ in range(3)]
        f = reference.encode(img)
        self.assertEqual(len(f), 64)

    def test_encode_many(self):
        img = [[[0.5 for _ in range(8)] for _ in range(8)] for _ in range(3)]
        fs = reference.encode_many([img, img])
        self.assertEqual(len(fs), 2)


class TestCrossAttention(unittest.TestCase):
    def test_decoupled(self):
        q = [[0.1] * 4 for _ in range(2)]
        tk = [[0.1] * 4 for _ in range(2)]
        tv = [[0.1] * 4 for _ in range(2)]
        ref_k, ref_v = cross_attention.make_ref_kv([[0.5] * 4])
        out = cross_attention.decoupled_cross_attention(q, (tk, tv), [(ref_k, ref_v)], [0.7])
        self.assertEqual(len(out), 2)


class TestWeighting(unittest.TestCase):
    def test_normalize(self):
        w = weighting.normalize_weights([], 3)
        self.assertAlmostEqual(sum(w), 1.0)

    def test_normalize_explicit(self):
        w = weighting.normalize_weights([0.7, 0.3], 2)
        self.assertAlmostEqual(sum(w), 1.0)


class TestModes(unittest.TestCase):
    def test_style(self):
        f = modes.apply_mode([[1.0, 2.0, 3.0]], "style")
        self.assertEqual(len(f[0]), 3)

    def test_unknown(self):
        with self.assertRaises(ValueError):
            modes.apply_mode([[1.0]], "bad")


if __name__ == "__main__":
    unittest.main()
