# -*- coding: utf-8 -*-
"""采样器基类与 Rectified Flow 轨迹构造。"""
from __future__ import annotations

from typing import Callable

# 速度场 v(x, t, cond) -> 与 x 同形状的向量
VelocityFn = Callable


class Trajectory:
    """把「噪声 -> 图像」拉直成直线：x_t = (1 - t) * x_0 + t * x_1。

    参数：
      x_0: 噪声（sigma_max 端）
      x_1: 目标图像（sigma_min 端）
    任意时刻 t，潜变量 x_t 沿直线插值；速度场 v = x_1 - x_0 恒定。
    """

    def __init__(self, x0, x1):
        self.x0 = x0
        self.x1 = x1

    def sample(self, t):
        if isinstance(t, (list, tuple)):
            return [self._at(float(ti)) for ti in t]
        return self._at(float(t))

    def _at(self, t):
        return _lerp(self.x0, self.x1, t)


def _lerp(a, b, t):
    if isinstance(a, (int, float)):
        return a + (b - a) * t
    if isinstance(a, list):
        return [_lerp(x, y, t) for x, y in zip(a, b)]
    raise TypeError("不支持的潜变量类型")


def add(a, b):
    """递归元素相加（支持任意嵌套深度的数值/列表）。"""
    if isinstance(a, (int, float)):
        return a + b
    return [add(x, y) for x, y in zip(a, b)]


def sub(a, b):
    if isinstance(a, (int, float)):
        return a - b
    return [sub(x, y) for x, y in zip(a, b)]


def scale(a, k):
    if isinstance(a, (int, float)):
        return a * k
    return [scale(x, k) for x in a]


def combine(a, b, wa=0.5):
    """wa*a + (1-wa)*b。"""
    if isinstance(a, (int, float)):
        return wa * a + (1 - wa) * b
    return [combine(x, y, wa) for x, y in zip(a, b)]


class Sampler:
    """采样器基类。子类实现 step()。"""

    name = "base"

    def __init__(self, num_steps: int = 12):
        self.num_steps = int(num_steps)

    def schedule(self):
        """返回 [0, 1] 内单调递减的 sigma 序列（从 sigma_max 到 sigma_min）。"""
        return [1.0 - i / max(self.num_steps - 1, 1) for i in range(self.num_steps)]

    def step(self, x, t, velocity: VelocityFn, cond, uncond=None, guidance: float = 4.5):
        raise NotImplementedError


class MockVelocity:
    """确定性 mock 速度场：把 x 朝目标方向匀速牵引，便于离线验证采样收敛。

    真实实现里 velocity = 神经网络输出；这里用闭式 v = target - x，使 flow 采样
    恰好收敛到 target，可用于无网络的环境下验证整套采样/CFG/批处理逻辑。
    """

    def __init__(self, target, strength: float = 1.0):
        self.target = target
        self.strength = strength

    def __call__(self, x, t, cond):
        return scale(sub(self.target, x), self.strength)
