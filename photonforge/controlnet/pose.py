# -*- coding: utf-8 -*-
"""姿态控制占位：接真实姿态估计（如 OpenPose）。"""
from __future__ import annotations


def extract(image):
    """返回关键点列表（占位实现）。"""
    h = len(image[0])
    w = len(image[0][0])
    # 返回若干网格关键点
    return [(y * h // 8, x * w // 8) for y in range(1, 8) for x in range(1, 8)]
