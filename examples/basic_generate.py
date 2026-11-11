# -*- coding: utf-8 -*-
"""基本文生图示例。"""
from photonforge.providers.base import get_provider

provider = get_provider("mock")
image = provider.generate(
    "一只戴红围巾的柴犬，冬日清晨，柔和逆光，4k，电影感",
    steps=8,
    width=512,
    height=512,
)
print(f"生成图像: {len(image[0])}x{len(image[0][0])}")

from photonforge.engine.image_io import tensor_to_ppm
tensor_to_ppm(image, "output.ppm")
print("已保存 output.ppm")
