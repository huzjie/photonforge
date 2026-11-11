# -*- coding: utf-8 -*-
"""多参考图风格迁移示例。"""
from photonforge.providers.base import get_provider

# 构造两张参考图（此处用占位张量；实际应读入真实参考图）
ref1 = [[[0.5] * 64 for _ in range(64)] for _ in range(3)]
ref2 = [[[0.3] * 64 for _ in range(64)] for _ in range(3)]

provider = get_provider("mock")
image = provider.generate(
    "城市夜景，霓虹风格",
    reference_images=[ref1, ref2],
    ref_weights=[0.7, 0.3],
    steps=8,
    width=512,
    height=512,
)
print("参考图融合生成完成:", len(image[0]), "x", len(image[0][0]))
