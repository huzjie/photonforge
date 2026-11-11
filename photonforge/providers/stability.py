# -*- coding: utf-8 -*-
"""Stability AI API 适配器。"""
from __future__ import annotations

import json
import urllib.request

from .base import BaseProvider
from ..registry import providers
from ..errors import ProviderError


@providers.register("stability")
class StabilityProvider(BaseProvider):
    name = "stability"

    def generate(self, prompt, reference_images=None, ref_weights=None, steps=12,
                 guidance=4.5, width=1024, height=1024, **kwargs):
        key = self.config.get("api_key")
        if not key:
            raise ProviderError("stability 需要 api_key")
        payload = {"prompt": prompt, "output_format": "png"}
        req = urllib.request.Request(
            "https://api.stability.ai/v2beta/stable-image/generate/core",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json",
                     "Accept": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=300) as r:
            return json.loads(r.read().decode("utf-8"))
