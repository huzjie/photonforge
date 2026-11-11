# -*- coding: utf-8 -*-
"""内容安全过滤器：提示词与图像的敏感内容拦截。"""
from __future__ import annotations

_BLOCKLIST = ["暴力", "血腥", "色情", "裸体", "赌博", "毒品", "仇恨", "歧视"]


def check_prompt(text: str):
    """检查提示词，返回 (是否安全, 命中词)。"""
    hits = [w for w in _BLOCKLIST if w in text]
    return (len(hits) == 0, hits)


def sanitize(text: str):
    """把敏感词替换为 [已过滤]。"""
    out = text
    for w in _BLOCKLIST:
        out = out.replace(w, "[已过滤]")
    return out


def check_image(image, threshold: float = 0.9):
    """简化的图像安全评分（真实实现是分类器；这里用亮度/方差启发式示意）。"""
    from ..tools.meta import stats
    st = stats(image)
    # 极低方差（纯色/异常）标记为可疑
    return st["var"] > 1e-6, st
