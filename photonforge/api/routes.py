# -*- coding: utf-8 -*-
"""路由。"""
from __future__ import annotations

import time

from fastapi import APIRouter

from ..providers.base import get_provider
from ..config import Config
from .schemas import GenerateRequest, EditRequest

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok", "service": "photonforge"}


@router.post("/generate")
def generate(req: GenerateRequest):
    provider = get_provider(Config.load().get("provider", "mock"))
    t0 = time.perf_counter()
    image = provider.generate(req.prompt, req.reference_images, req.ref_weights,
                              req.steps, req.guidance, req.width, req.height)
    elapsed = time.perf_counter() - t0
    return {"status": "ok", "image": image, "elapsed": elapsed}


@router.post("/edit")
def edit(req: EditRequest):
    provider = get_provider(Config.load().get("provider", "mock"))
    t0 = time.perf_counter()
    image = provider.edit(req.instruction, req.image, strength=req.strength)
    elapsed = time.perf_counter() - t0
    return {"status": "ok", "image": image, "elapsed": elapsed}
