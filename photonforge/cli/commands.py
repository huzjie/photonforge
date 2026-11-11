# -*- coding: utf-8 -*-
"""CLI 命令实现。"""
from __future__ import annotations

import time


def cmd_gen(args):
    from ..providers.base import get_provider
    from ..config import Config
    provider = get_provider(args.provider or Config.load().get("provider", "mock"))
    t0 = time.perf_counter()
    image = provider.generate(args.prompt, args.reference, args.ref_weight,
                              args.steps, args.guidance, args.width, args.height)
    elapsed = time.perf_counter() - t0
    _save(image, args.out)
    print(f"生成完成: {args.out}（{len(image[0])}x{len(image[0][0])}，{elapsed:.2f}s）")
    return 0


def cmd_edit(args):
    from ..engine.image_io import ppm_to_tensor
    from ..providers.base import get_provider
    from ..config import Config
    provider = get_provider(Config.load().get("provider", "mock"))
    image = ppm_to_tensor(args.input)
    out = provider.edit(args.instruct, image)
    _save(out, args.out)
    print(f"编辑完成: {args.out}")
    return 0


def cmd_inpaint(args):
    from ..engine.image_io import ppm_to_tensor
    from ..edit.inpaint import inpaint
    from ..edit.mask import from_points
    from ..flux.base import MockVelocity
    from ..utils import rng
    image = ppm_to_tensor(args.input)
    h = len(image[0])
    w = len(image[0][0])
    r = rng(args.prompt)
    target = [[[r.random() for _ in range(w)] for _ in range(h)] for _ in range(len(image))]
    vf = MockVelocity(target)
    m = from_points(h, w, [(h // 2, w // 2)], radius=8)
    out = inpaint(image, m, vf, args.prompt)
    _save(out, args.out)
    print(f"重绘完成: {args.out}")
    return 0


def cmd_serve(args):
    from ..api.server import run
    run(args.host, args.port)
    return 0


def cmd_benchmark(args):
    from ..providers.base import get_provider
    from ..config import Config
    provider = get_provider(Config.load().get("provider", "mock"))
    times = []
    for _ in range(args.runs):
        t0 = time.perf_counter()
        provider.generate(args.prompt, steps=args.steps, width=256, height=256)
        times.append(time.perf_counter() - t0)
    avg = sum(times) / len(times)
    print(f"基准: {args.runs} 次，平均 {avg*1000:.1f} ms/张")
    return 0


def _save(image, path):
    if path.endswith(".png"):
        from ..engine.image_io import to_png
        to_png(image, path)
    else:
        from ..engine.image_io import tensor_to_ppm
        tensor_to_ppm(image, path)
