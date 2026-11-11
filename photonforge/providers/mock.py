# -*- coding: utf-8 -*-
"""mock provider：离线确定性后端，零依赖验证完整链路。"""
from __future__ import annotations

from .base import BaseProvider
from ..registry import providers


@providers.register("mock")
class MockProvider(BaseProvider):
    name = "mock"

    def __init__(self, config=None):
        super().__init__(config)

    def generate(self, prompt, reference_images=None, ref_weights=None, steps=12,
                 guidance=4.5, width=1024, height=1024, **kwargs):
        from ..engine.pipeline import GenerationPipeline
        pipe = GenerationPipeline(self.config)
        return pipe.generate(prompt, reference_images, ref_weights, steps, guidance, width, height)

    def edit(self, instruction, image, **kwargs):
        from ..engine.pipeline import GenerationPipeline
        from ..flux.base import MockVelocity
        from ..utils import rng
        r = rng(instruction)
        target = [[[r.random() for _ in range(len(image[0][0]))] for _ in range(len(image[0]))] for _ in range(len(image))]
        vf = MockVelocity(target)
        from ..edit.instruct import apply_instruction
        return apply_instruction(image, instruction, vf, instruction, kwargs.get("strength", 0.75))
