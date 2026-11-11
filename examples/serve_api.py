# -*- coding: utf-8 -*-
"""REST API 调用示例。"""
from photonforge.sdk.client import PhotonforgeClient

client = PhotonforgeClient("http://127.0.0.1:8000")
print("健康检查:", client.health())
resp = client.generate("一只柴犬", steps=8, width=256, height=256)
print("生成结果状态:", resp["status"], "耗时:", round(resp["elapsed"], 2), "s")
