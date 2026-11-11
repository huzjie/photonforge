# -*- coding: utf-8 -*-
"""隐形水印：在图像最低有效位写入可校验的签名，便于溯源。"""
from __future__ import annotations

import hashlib


def embed_bits(image, payload: str):
    """把 payload 的哈希嵌入图像 LSB（示意性实现，逐像素最低位）。"""
    sig = hashlib.sha256(payload.encode("utf-8")).digest()
    bits = []
    for b in sig:
        for i in range(8):
            bits.append((b >> i) & 1)
    c = len(image)
    h = len(image[0])
    w = len(image[0][0])
    out = [[[0.0 for _ in range(w)] for _ in range(h)] for _ in range(c)]
    for cc in range(c):
        for y in range(h):
            for x in range(w):
                idx = (cc * h + y) * w + x
                v = image[cc][y][x]
                if idx < len(bits):
                    # 修改 LSB
                    v = (int(v * 255) & 0xFE | bits[idx]) / 255.0
                out[cc][y][x] = v
    return out


def verify(image, payload: str):
    """校验水印是否匹配（返回匹配位数占比）。"""
    sig = hashlib.sha256(payload.encode("utf-8")).digest()
    bits = []
    for b in sig:
        for i in range(8):
            bits.append((b >> i) & 1)
    c = len(image)
    h = len(image[0])
    w = len(image[0][0])
    match = 0
    total = 0
    for cc in range(c):
        for y in range(h):
            for x in range(w):
                idx = (cc * h + y) * w + x
                if idx < len(bits):
                    lsb = int(image[cc][y][x] * 255) & 1
                    if lsb == bits[idx]:
                        match += 1
                    total += 1
    return match / max(total, 1)
