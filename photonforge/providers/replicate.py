# -*- coding: utf-8 -*-
"""Replicate 托管 API 适配器。"""
from __future__ import annotations

import json
import urllib.request

from .base import BaseProvider
from ..registry import providers
from ..errors import ProviderError


@providers.register("replicate")
class ReplicateProvider(BaseProvider):
    name = "replicate"

    def generate(self, prompt, reference_images=None, ref_weights=None, steps=12,
                 guidance=4.5, width=1024, height=1024, **kwargs):
        key = self.config.get("api_key")
        if not key:
            raise ProviderError("replicate 需要 api_key")
        model = self.config.get("model", "black-forest-labs/flux-schnell")
        payload = {"input": {"prompt": prompt, "num_outputs": 1}}
        req = urllib.request.Request(
            "https://api.replicate.com/v1/models/" + model + "/predictions",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=300) as r:
            return json.loads(r.read().decode("utf-8"))
