# -*- coding: utf-8 -*-
"""providers 子系统：多后端适配器（mock/minimax/diffusers/comfyui/a1111/openai）。"""
from __future__ import annotations

from . import mock, minimax, diffusers, comfyui, a1111, openai
from .base import BaseProvider
from ..registry import providers

__all__ = ["BaseProvider", "mock", "minimax", "diffusers", "comfyui", "a1111", "openai"]
