# -*- coding: utf-8 -*-
"""OpenAI 图像 API 适配器（兼容）。"""
from __future__ import annotations

import json
import urllib.request

from .base import BaseProvider
from ..registry import providers
from ..errors import ProviderError


@providers.register("openai")
class OpenAIProvider(BaseProvider):
    name = "openai"
    DEFAULT_BASE = "https://api.openai.com/v1"

    def generate(self, prompt, reference_images=None, ref_weights=None, steps=12,
                 guidance=4.5, width=1024, height=1024, **kwargs):
        base = self.config.get("base_url") or self.DEFAULT_BASE
        key = self.config.get("api_key")
        if not key:
            raise ProviderError("openai provider 需要 api_key")
        payload = {"model": self.config.get("model", "gpt-image-1"), "prompt": prompt,
                   "size": "1024x1024"}
        req = urllib.request.Request(
            f"{base}/images/generations",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=300) as r:
            return json.loads(r.read().decode("utf-8"))
