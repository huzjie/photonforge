# -*- coding: utf-8 -*-
"""Automatic1111 (Stable Diffusion WebUI) 适配器。"""
from __future__ import annotations

import base64
import json
import urllib.request

from .base import BaseProvider
from ..registry import providers
from ..errors import ProviderError


@providers.register("a1111")
class A1111Provider(BaseProvider):
    name = "a1111"

    def generate(self, prompt, reference_images=None, ref_weights=None, steps=12,
                 guidance=4.5, width=1024, height=1024, **kwargs):
        base = self.config.get("base_url") or "http://127.0.0.1:7860"
        payload = {
            "prompt": prompt,
            "steps": steps,
            "cfg_scale": guidance,
            "width": width,
            "height": height,
        }
        req = urllib.request.Request(
            f"{base}/sdapi/v1/txt2img",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=300) as r:
            data = json.loads(r.read().decode("utf-8"))
        return {"images_base64": data.get("images", [])}
