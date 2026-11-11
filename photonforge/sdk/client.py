# -*- coding: utf-8 -*-
"""Python SDK：HTTP 客户端。"""
from __future__ import annotations

import json
import urllib.request


class PhotonforgeClient:
    def __init__(self, base_url="http://127.0.0.1:8000", token=None):
        self.base_url = base_url.rstrip("/")
        self.token = token

    def _post(self, path, payload):
        req = urllib.request.Request(
            self.base_url + path,
            data=json.dumps(payload).encode("utf-8"),
            headers=self._headers(),
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=600) as r:
            return json.loads(r.read().decode("utf-8"))

    def _headers(self):
        h = {"Content-Type": "application/json"}
        if self.token:
            h["Authorization"] = f"Bearer {self.token}"
        return h

    def health(self):
        with urllib.request.urlopen(self.base_url + "/health", timeout=30) as r:
            return json.loads(r.read().decode("utf-8"))

    def generate(self, prompt, reference_images=None, ref_weights=None, steps=12,
                 guidance=4.5, width=1024, height=1024):
        return self._post("/generate", {
            "prompt": prompt,
            "reference_images": reference_images or [],
            "ref_weights": ref_weights or [],
            "steps": steps,
            "guidance": guidance,
            "width": width,
            "height": height,
        })

    def edit(self, instruction, image, strength=0.75):
        return self._post("/edit", {"instruction": instruction, "image": image,
                                    "strength": strength})
