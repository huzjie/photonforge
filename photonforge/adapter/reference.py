# -*- coding: utf-8 -*-
"""参考图编码：把参考图编码成语义特征向量，供解耦交叉注意力使用。"""
from __future__ import annotations

import math


def encode(image, feat_dim: int = 64):
    """确定性参考图编码：对图像做分块均值，投影到固定维特征。

    真实实现是 CLIP 图像编码器；这里用分块池化 + 确定性投影模拟，
    保证零依赖、可复现，且能反映不同参考图之间的语义差异。
    """
    C = len(image)
    H = len(image[0])
    W = len(image[0][0])
    # 分块池化到 8x8 网格，再压平
    gh, gw = 8, 8
    feats = []
    for gy in range(gh):
        for gx in range(gw):
            acc = [0.0] * C
            cnt = 0
            for y in range(gy * H // gh, (gy + 1) * H // gh):
                for x in range(gx * W // gw, (gx + 1) * W // gw):
                    for c in range(C):
                        acc[c] += image[c][y][x]
                    cnt += 1
            for c in range(C):
                acc[c] /= max(cnt, 1)
            feats.append(sum(acc) / C)
    # 确定性投影到 feat_dim
    out = []
    for i in range(feat_dim):
        v = 0.0
        for j, f in enumerate(feats):
            v += f * math.sin((i + 1) * (j + 1) * 0.01)
        out.append(math.tanh(v / max(len(feats), 1)))
    return out


def encode_many(images, feat_dim: int = 64):
    return [encode(img, feat_dim) for img in images]
