# -*- coding: utf-8 -*-
"""用 mock 生成确定性训练数据集。"""
import json
from photonforge.providers.base import get_provider

provider = get_provider("mock")
dataset = []
for i in range(20):
    img = provider.generate(f"样本 {i}", steps=4, width=32, height=32)
    dataset.append({"id": i, "prompt": f"样本 {i}", "image": img})
with open("dataset.json", "w", encoding="utf-8") as f:
    json.dump(dataset, f, ensure_ascii=False)
print("生成 dataset.json（20 条）")
