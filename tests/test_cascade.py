# -*- coding: utf-8 -*-
import unittest

from photonforge.cascade import stage, upsampler, tiled, scheduler
from photonforge.flux.base import MockVelocity


class TestCascade(unittest.TestCase):
    def test_low_res_generate(self):
        target = [[[0.0] * 4 for _ in range(4)] for _ in range(2)]
        lat = stage.low_res_generate(MockVelocity(target), ["c"], (2, 4, 4), steps=2)
        self.assertEqual(len(lat[0]), 4)

    def test_upscale(self):
        low = [[[1.0] * 2 for _ in range(2)] for _ in range(2)]
        up = upsampler.upscale_to_4k(low, target=32, latent_scale=8)
        self.assertEqual(len(up[0]), 4)

    def test_tiled_decode(self):
        lat = [[[0.5] * 32 for _ in range(32)] for _ in range(4)]
        img = tiled.tiled_decode(lat, tile_size=8, scale=8)
        self.assertEqual(len(img[0]), 256)

    def test_pipeline(self):
        p = scheduler.CascadePipeline(low_res=64, high_res=128, refine_steps=1, tiled_4k=False)
        target = [[[0.0] * 16 for _ in range(16)] for _ in range(4)]
        img = p.run(MockVelocity(target), [0.1] * 8)
        self.assertEqual(len(img[0]), 128)


if __name__ == "__main__":
    unittest.main()
