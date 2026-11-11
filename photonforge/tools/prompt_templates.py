# -*- coding: utf-8 -*-
"""提示词模板库：风格 / 构图 / 质感 / 电影感。"""
from __future__ import annotations

STYLES = {
    "photoreal": "超写实摄影，真实光影，皮肤纹理清晰，85mm 镜头",
    "cinematic": "电影感，宽银幕，浅景深，胶片颗粒，冷暖对比",
    "anime": "日系动漫风格，赛璐璐上色，干净线条，明快色彩",
    "watercolor": "水彩画，柔和晕染，留白，清新通透",
    "oil": "油画质感，厚涂笔触，古典色调，细节丰富",
    "cyberpunk": "赛博朋克，霓虹灯，未来都市，高对比，冷色调",
}

QUALITY = {
    "low": "",
    "medium": "细节丰富，构图平衡",
    "high": "细节丰富，构图平衡，8k，最佳画质，大师级作品",
}

LIGHTING = {
    "soft": "柔和逆光",
    "golden": "黄金时刻，暖色调侧光",
    "studio": "棚拍布光，均匀柔和",
    "dramatic": "戏剧性光影，明暗对比",
}


def build(style="photoreal", quality="high", lighting="soft", subject="", extra=""):
    parts = []
    if subject:
        parts.append(subject)
    parts.append(STYLES.get(style, ""))
    parts.append(LIGHTING.get(lighting, ""))
    parts.append(QUALITY.get(quality, ""))
    if extra:
        parts.append(extra)
    return "，".join(p for p in parts if p)
