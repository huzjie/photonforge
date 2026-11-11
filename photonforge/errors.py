# -*- coding: utf-8 -*-
"""错误类型定义。"""
from __future__ import annotations


class PhotonforgeError(Exception):
    """基础异常。"""


class ConfigError(PhotonforgeError):
    """配置错误。"""


class ProviderError(PhotonforgeError):
    """后端调用错误。"""


class GenerationError(PhotonforgeError):
    """生成失败。"""


class UnsupportedFeature(PhotonforgeError):
    """不支持的特性。"""
