# -*- coding: utf-8 -*-
"""HuggingFace diffusers 适配器。"""
from __future__ import annotations

from .base import BaseProvider
from ..registry import providers
from ..errors import ProviderError


@providers.register("diffusers")
class DiffusersProvider(BaseProvider):
    name = "diffusers"

    def generate(self, prompt, reference_images=None, ref_weights=None, steps=12,
                 guidance=4.5, width=1024, height=1024, **kwargs):
        try:
            import torch  # noqa
        except ImportError as e:
            raise ProviderError("diffusers 需要 torch（pip install diffusers torch）") from e
        model_id = self.config.get("model", "stabilityai/stable-diffusion-xl-base-1.0")
        from diffusers import DiffusionPipeline  # noqa
        pipe = DiffusionPipeline.from_pretrained(model_id)
        result = pipe(prompt=prompt, num_inference_steps=steps, guidance_scale=guidance,
                      width=width, height=height)
        return {"images": result.images}
