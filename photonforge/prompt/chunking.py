# -*- coding: utf-8 -*-
"""长提示词分块：超出编码器长度的提示词切成多块。"""
from __future__ import annotations

import re


def chunk_by_chars(text: str, chunk_size: int = 512):
    """按字符数分块，尽量在标点处断开。"""
    if len(text) <= chunk_size:
        return [text]
    chunks = []
    remaining = text
    while len(remaining) > chunk_size:
        cut = remaining.rfind(",", 0, chunk_size)
        if cut < chunk_size // 2:
            cut = remaining.rfind("。", 0, chunk_size)
        if cut < chunk_size // 2:
            cut = remaining.rfind(" ", 0, chunk_size)
        if cut < chunk_size // 2:
            cut = chunk_size
        chunks.append(remaining[:cut].strip())
        remaining = remaining[cut:].lstrip(", 。")
    if remaining.strip():
        chunks.append(remaining.strip())
    return chunks


def chunk_by_tokens(tokens, chunk_size: int = 512):
    return [tokens[i:i + chunk_size] for i in range(0, len(tokens), chunk_size)]
