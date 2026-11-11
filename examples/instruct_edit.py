# -*- coding: utf-8 -*-
"""指令编辑示例。"""
from photonforge.providers.base import get_provider
from photonforge.engine.image_io import ppm_to_tensor

provider = get_provider("mock")
image = ppm_to_tensor("input.ppm") if __import__("os").path.exists("input.ppm") \
    else [[[0.5] * 128 for _ in range(128)] for _ in range(3)]

edited = provider.edit("把背景换成雪地", image, strength=0.6)
print("编辑完成:", len(edited[0]), "x", len(edited[0][0]))
