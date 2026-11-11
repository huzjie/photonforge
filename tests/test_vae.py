# -*- coding: utf-8 -*-
import unittest

from photonforge.vae import encoder, decoder, kl, vq, resize


class TestVAE(unittest.TestCase):
    def test_encode_decode_roundtrip_shape(self):
        img = [[[0.5 for _ in range(16)] for _ in range(16)] for _ in range(3)]
        lat = encoder.encode(img, scale=8)
        self.assertEqual(len(lat[0]), 2)
        dec = decoder.decode(lat, scale=8)
        self.assertEqual(len(dec[0]), 16)

    def test_kl(self):
        self.assertGreater(kl.kl_divergence([0.0], [0.0]), -1e-6)

    def test_vq(self):
        cb = vq.init_codebook(16, 4)
        idx = vq.quantize(cb, [[0.0, 0.0, 0.0, 0.0], [1.0, 0.0, 0.0, 0.0]])
        self.assertEqual(len(idx), 2)
        dec = vq.dequantize(cb, idx)
        self.assertEqual(len(dec), 2)

    def test_resize(self):
        img = [[[1.0 for _ in range(4)] for _ in range(4)] for _ in range(1)]
        up = resize.nearest_neighbor(img, 2)
        self.assertEqual(len(up[0]), 8)
        down = resize.downsample_avg(up, 2)
        self.assertEqual(len(down[0]), 4)


if __name__ == "__main__":
    unittest.main()
