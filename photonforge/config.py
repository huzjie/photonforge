# -*- coding: utf-8 -*-
"""配置加载：优先级 默认值 < config.yaml < 环境变量 PF_*。零第三方依赖。"""
from __future__ import annotations

import os
from typing import Any


_DEFAULTS: dict[str, Any] = {
    "home": "~/.photonforge",
    "provider": "mock",
    "model": "h3-image-mock",
    "api_key": None,
    "base_url": None,
    "flux.steps": 12,
    "flux.sampler": "heun",
    "flux.guidance": 4.5,
    "flux.sigma_min": 0.0,
    "flux.sigma_max": 1.0,
    "flux.straightness": 1.0,
    "dit.patch_size": 2,
    "dit.hidden_size": 512,
    "dit.depth": 12,
    "dit.num_heads": 8,
    "dit.mlp_ratio": 4.0,
    "dit.rope_theta": 10000.0,
    "vae.latent_scale": 8,
    "vae.latent_channels": 4,
    "vae.quantize": "kl",
    "vae.codebook_size": 16384,
    "adapter.max_references": 16,
    "adapter.ref_weights": [],
    "adapter.mode": "style",
    "adapter.cross_attn_scale": 1.0,
    "prompt.encoder": "t5",
    "prompt.max_length": 7500,
    "prompt.chunk_size": 512,
    "prompt.enable_weighting": True,
    "cascade.low_res": 512,
    "cascade.high_res": 4096,
    "cascade.refine_steps": 4,
    "cascade.tiled_4k": True,
    "edit.blend_mode": "feather",
    "edit.mask_blur": 8,
    "edit.strength": 0.75,
    "api.host": "127.0.0.1",
    "api.port": 8000,
    "api.auth_token": None,
    "api.max_batch_size": 16,
}


class Config:
    """扁平键访问的配置对象。键用点号分层，如 `flux.steps`。"""

    def __init__(self, data: dict[str, Any]):
        self._data = dict(data)

    @classmethod
    def load(cls, path: str | None = None) -> "Config":
        data = dict(_DEFAULTS)
        if path and os.path.exists(path):
            data.update(_read_yaml_flat(path))
        for key in list(_DEFAULTS):
            env = "PF_" + key.replace(".", "_").upper()
            if env in os.environ:
                data[key] = _coerce(os.environ[env])
        return cls(data)

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def as_dict(self) -> dict[str, Any]:
        return dict(self._data)


def _coerce(raw: str) -> Any:
    s = raw.strip()
    if s.lower() in ("true", "false"):
        return s.lower() == "true"
    if s.lower() in ("null", "none", ""):
        return None
    try:
        return int(s)
    except ValueError:
        pass
    try:
        return float(s)
    except ValueError:
        pass
    return raw


def _read_yaml_flat(path: str) -> dict[str, Any]:
    """极简 YAML 子集解析（仅支持 2 层缩进映射），避免引入 pyyaml 依赖。"""
    out: dict[str, Any] = {}
    section: str | None = None
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if line.startswith(" ") or line.startswith("\t"):
                if section and ":" in stripped:
                    k, v = stripped.split(":", 1)
                    out[f"{section}.{k.strip()}"] = _coerce(v.strip().strip("\"'").rstrip('\"'))
            else:
                if ":" in stripped:
                    k, v = stripped.split(":", 1)
                    v = v.strip()
                    if v == "":
                        section = k.strip()
                    else:
                        out[k.strip()] = _coerce(v.strip().strip("\"'"))
    return out
