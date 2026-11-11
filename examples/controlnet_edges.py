# -*- coding: utf-8 -*-
"""ControlNet 边缘控制示例。"""
from photonforge.controlnet import canny
from photonforge.engine.image_io import ppm_to_tensor

image = ppm_to_tensor("input.ppm")
edges = canny.extract(image)
print("边缘提取完成:", len(edges), "x", len(edges[0]))
