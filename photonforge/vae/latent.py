# -*- coding: utf-8 -*-
"""潜空间张量工具。"""
from __future__ import annotations


def zeros(channels, height, width):
    return [[[0.0 for _ in range(width)] for _ in range(height)] for _ in range(channels)]


def shape(latent):
    return (len(latent), len(latent[0]), len(latent[0][0]))


def flatten(latent):
    out = []
    for c in latent:
        for row in c:
            out.extend(row)
    return out


def mean_abs(latent):
    flat = flatten(latent)
    return sum(abs(v) for v in flat) / max(len(flat), 1)
