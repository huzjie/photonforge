# -*- coding: utf-8 -*-
"""隐形水印示例。"""
from photonforge.safety import watermark
from photonforge.providers.base import get_provider

image = get_provider("mock").generate("一只柴犬", steps=4, width=64, height=64)
watermarked = watermark.embed_bits(image, "huzjie-2026-11-11")
print("水印嵌入完成，校验匹配度:", round(watermark.verify(watermarked, "huzjie-2026-11-11"), 4))
