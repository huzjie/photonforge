# -*- coding: utf-8 -*-
"""ComfyUI 工作流 API 适配器。"""
from __future__ import annotations

import json
import urllib.request

from .base import BaseProvider
from ..registry import providers
from ..errors import ProviderError


@providers.register("comfyui")
class ComfyUIProvider(BaseProvider):
    name = "comfyui"

    def generate(self, prompt, reference_images=None, ref_weights=None, steps=12,
                 guidance=4.5, width=1024, height=1024, **kwargs):
        base = self.config.get("base_url") or "http://127.0.0.1:8188"
        workflow = {
            "prompt": prompt,
            "steps": steps,
            "cfg": guidance,
            "width": width,
            "height": height,
        }
        req = urllib.request.Request(
            f"{base}/prompt",
            data=json.dumps(workflow).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=300) as r:
            return json.loads(r.read().decode("utf-8"))
