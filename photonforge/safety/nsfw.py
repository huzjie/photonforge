# -*- coding: utf-8 -*-
"""NSFW 检测占位：接真实分类器（如 CLIP-based / NudeNet）。"""
from __future__ import annotations


def detect(image):
    """返回 (是否包含不适宜内容, 置信度)。默认放行，接真实模型后替换。"""
    return False, 0.0
