# -*- coding: utf-8 -*-
"""参考图注入模式：style / face / composition / mixed。"""
from __future__ import annotations

MODES = ("style", "face", "composition", "mixed")


def apply_mode(feats, mode: str):
    """按模式处理参考图特征。

    - style: 强调全局风格，取特征均值
    - face: 强调局部一致，保留高频（差分）
    - composition: 强调空间布局，取网格顺序
    - mixed: 混合风格与构图
    """
    if mode == "style":
        return [_mean(f) for f in feats]
    if mode == "face":
        return [_highpass(f) for f in feats]
    if mode == "composition":
        return feats
    if mode == "mixed":
        return [list(f) for f in feats]
    raise ValueError(f"未知模式: {mode!r}（可用 {MODES}）")


def _mean(f):
    return [sum(f) / max(len(f), 1)] * len(f)


def _highpass(f):
    return [f[i] - f[i - 1] if i > 0 else f[i] for i in range(len(f))]
