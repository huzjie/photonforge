# -*- coding: utf-8 -*-
"""局部重绘：只在蒙版区域重新生成。"""
from __future__ import annotations

from . import mask as masklib, blend


def inpaint(image, mask, velocity_fn, cond, mask_blur: int = 8, strength: float = 0.75):
    """在蒙版区域重绘，其余区域保留原图。"""
    from .. import vae
    m = masklib.blur(mask, mask_blur)
    # 全图重生成
    latent = vae.encoder.encode(image)
    edited = velocity_fn(latent, 0.5, cond)
    regenerated = vae.decoder.decode(edited)
    return blend.feather_blend(image, regenerated, m)
