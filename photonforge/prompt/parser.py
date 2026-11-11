# -*- coding: utf-8 -*-
"""提示词解析：权重语法 (词:1.3)、[词] 降权、分段。"""
from __future__ import annotations

import re


def parse_weights(text: str):
    """解析 (词:权重) 语法，返回 [(片段, 权重)]。"""
    segments = []
    pattern = re.compile(r"\(([^()]*?)(?::([0-9.]+))?\)")
    pos = 0
    for m in pattern.finditer(text):
        if m.start() > pos:
            segments.append((text[pos:m.start()], 1.0))
        inner = m.group(1)
        w = float(m.group(2)) if m.group(2) else 1.1
        segments.append((inner, w))
        pos = m.end()
    if pos < len(text):
        segments.append((text[pos:], 1.0))
    return segments


def strip_weighting(text: str) -> str:
    """去掉权重语法，得到纯文本。"""
    return re.sub(r"\(([^()]*?)(?::[0-9.]+)?\)", r"\1", text)
