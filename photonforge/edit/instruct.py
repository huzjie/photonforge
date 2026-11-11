# -*- coding: utf-8 -*-
"""指令编辑：把「把背景换成雪地」这类自然语言指令转成可执行的编辑操作。"""
from __future__ import annotations

import re

_INSTRUCTIONS = {
    "背景": "background",
    "颜色": "color",
    "色调": "tone",
    "风格": "style",
    "天气": "weather",
    "光照": "lighting",
}


def parse_instruction(text: str):
    """解析自然语言指令，返回 (操作类型, 目标参数)。"""
    for zh, op in _INSTRUCTIONS.items():
        if zh in text:
            return op, text
    return "general", text


def apply_instruction(image, instruction: str, velocity_fn, cond, strength: float = 0.75):
    """简化的指令编辑：把指令作为条件追加，对图像做一次带强度的重生成。"""
    from .. import vae
    op, _ = parse_instruction(instruction)
    # 编码 -> 潜空间扰动 -> 解码
    latent = vae.encoder.encode(image)
    c = len(latent)
    h = len(latent[0])
    w = len(latent[0][0])
    # 用 velocity 场做一次带强度的推进（模拟编辑）
    edited = velocity_fn(latent, 0.5, cond + "|" + instruction)
    out = vae.decoder.decode(edited)
    return blend_edit(image, out, strength)


def blend_edit(base, edit, strength):
    from . import blend
    return blend.alpha_blend(base, edit, strength)
