# -*- coding: utf-8 -*-
"""批量导出 PPM 示例。"""
import sys
from photonforge.providers.base import get_provider

provider = get_provider("mock")
for i in range(4):
    img = provider.generate(f"风格 {i}", steps=4, width=64, height=64)
    from photonforge.engine.image_io import tensor_to_ppm
    tensor_to_ppm(img, f"out_{i}.ppm")
    print("导出 out_%d.ppm" % i)
