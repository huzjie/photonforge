# -*- coding: utf-8 -*-
"""生成流水线：把八个子系统串成端到端文生图。"""
from __future__ import annotations

from .. import flux, dit, vae, adapter, prompt, cascade, edit


class GenerationPipeline:
    """端到端文生图流水线。可离线（mock）运行完整链路。"""

    def __init__(self, config=None):
        from ..config import Config
        self.config = config or Config.load()

    def generate(self, text: str, reference_images=None, ref_weights=None, steps: int = 12,
                 guidance: float = 4.5, width: int = 1024, height: int = 1024):
        """文生图。reference_images: 可选参考图列表。"""
        # 1. 提示词编码（长文本分块 + 池化）
        cond = prompt.t5.encode_long(text)
        # 2. 参考图注入
        ref_feats = []
        if reference_images:
            ref_feats = adapter.reference.encode_many(reference_images)
        # 3. 确定性 mock 速度场（真实后端替换为神经网络）
        import random
        from ..utils import rng
        r = rng(text + str(reference_images is not None))
        target = self._make_target(width // 8, height // 8, text, r)
        velocity = flux.base.MockVelocity(target)
        # 4. 级联生成（低分辨率 -> 4K 细化 -> 解码）
        pipeline = cascade.scheduler.CascadePipeline(
            low_res=512, high_res=4096, refine_steps=4, tiled_4k=True)
        image = pipeline.run(velocity, cond, channels=4)
        # 5. 裁剪到目标尺寸
        return self._crop(image, height, width)

    def _make_target(self, w, h, text, r):
        """确定性目标潜变量（mock）。"""
        c = 4
        out = vae.latent.zeros(c, h, w)
        seed = sum(ord(ch) for ch in text)
        for cc in range(c):
            for y in range(h):
                for x in range(w):
                    out[cc][y][x] = ((seed * (cc + 1) * (y + 1) * (x + 1)) % 1000) / 1000.0
        return out

    def _crop(self, image, height, width):
        c = len(image)
        h = len(image[0])
        w = len(image[0][0])
        out = vae.latent.zeros(c, height, width)
        for cc in range(c):
            for y in range(height):
                for x in range(width):
                    out[cc][y][x] = image[cc][min(y, h - 1)][min(x, w - 1)]
        return out
