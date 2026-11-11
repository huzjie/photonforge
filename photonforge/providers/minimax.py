# -*- coding: utf-8 -*-
"""MiniMax H3 Image API 适配器（真实后端）。"""
from __future__ import annotations

import json
import urllib.request

from .base import BaseProvider
from ..registry import providers
from ..errors import ProviderError


@providers.register("minimax")
class MiniMaxProvider(BaseProvider):
    name = "minimax"
    DEFAULT_BASE = "https://api.minimax.io/v1"

    def generate(self, prompt, reference_images=None, ref_weights=None, steps=12,
                 guidance=4.5, width=1024, height=1024, **kwargs):
        base = self.config.get("base_url") or self.DEFAULT_BASE
        key = self.config.get("api_key")
        if not key:
            raise ProviderError("MiniMax provider 需要 api_key（PF_API_KEY）")
        payload = {
            "model": self.config.get("model", "h3-image"),
            "prompt": prompt,
            "width": width,
            "height": height,
            "steps": steps,
            "guidance_scale": guidance,
        }
        if reference_images:
            payload["reference_images"] = reference_images
            payload["ref_weights"] = ref_weights or []
        req = urllib.request.Request(
            f"{base}/image/generation",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=300) as r:
            return json.loads(r.read().decode("utf-8"))
