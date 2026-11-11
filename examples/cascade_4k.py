# -*- coding: utf-8 -*-
"""级联 4K 生成示例。"""
from photonforge.cascade.scheduler import CascadePipeline
from photonforge.flux.base import MockVelocity
from photonforge.prompt.t5 import encode_long

cond = encode_long("蒸汽朋克城市夜景，赛博霓虹，细节丰富")
target = [[[0.0] * 512 for _ in range(512)] for _ in range(4)]

pipe = CascadePipeline(low_res=512, high_res=4096, refine_steps=4, tiled_4k=True)
image = pipe.run(MockVelocity(target), cond)
print("4K 生成完成:", len(image[0]), "x", len(image[0][0]))
