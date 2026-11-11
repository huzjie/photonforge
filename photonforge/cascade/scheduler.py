# -*- coding: utf-8 -*-
"""级联调度：编排低分辨率生成 + 高分辨率细化的完整流程。"""
from __future__ import annotations

from . import stage, upsampler, tiled


class CascadePipeline:
    """完整级联流水线：low_res -> upsample -> refine -> decode(4K)。"""

    def __init__(self, low_res: int = 512, high_res: int = 4096, refine_steps: int = 4,
                 latent_scale: int = 8, tiled_4k: bool = True):
        self.low_res = low_res
        self.high_res = high_res
        self.refine_steps = refine_steps
        self.latent_scale = latent_scale
        self.tiled_4k = tiled_4k

    def run(self, velocity_fn, cond, channels: int = 4):
        lh = self.low_res // self.latent_scale
        lw = self.low_res // self.latent_scale
        low_lat = stage.low_res_generate(velocity_fn, cond, (channels, lh, lw))
        high_lat = upsampler.upscale_to_4k(low_lat, self.high_res, self.latent_scale)
        refined = stage.refine(high_lat, velocity_fn, cond, self.refine_steps)
        if self.tiled_4k:
            return tiled.tiled_decode(refined, scale=self.latent_scale)
        from .. import vae
        return vae.decoder.decode(refined, self.latent_scale)
