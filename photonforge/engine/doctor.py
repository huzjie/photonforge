# -*- coding: utf-8 -*-
"""doctor 自检：逐子系统诊断。"""
from __future__ import annotations

CHECKS = [
    ("flux", "采样器"),
    ("dit", "DiT 主干"),
    ("vae", "潜空间"),
    ("adapter", "多参考图"),
    ("prompt", "长提示词"),
    ("cascade", "级联 4K"),
    ("edit", "编辑"),
    ("engine", "流水线"),
]


def run_doctor(verbose: bool = True):
    results = []
    for name, desc in CHECKS:
        try:
            ok = _check(name)
            results.append((name, desc, ok))
        except Exception as e:  # noqa
            results.append((name, desc, False))
            if verbose:
                print(f"[{name}] 检查异常: {e}")
    passed = sum(1 for _, _, ok in results if ok)
    if verbose:
        for name, desc, ok in results:
            mark = "OK" if ok else "FAIL"
            print(f"  [{mark}] {name:<10} {desc}")
        print(f"自检完成: {passed}/{len(results)} 通过")
    return passed == len(results)


def _check(name):
    from ..utils import rng
    if name == "flux":
        from ..flux.euler import EulerSampler
        from ..flux.base import MockVelocity
        s = EulerSampler(4)
        x = 0.0
        for t in s.schedule():
            x = s.step(x, t, MockVelocity(1.0), "c")
        return isinstance(x, (int, float))
    if name == "dit":
        from ..dit import patchify, block
        toks = patchify.patchify([[[1.0, 2.0], [3.0, 4.0]]])
        out = block.dit_block(toks, [0.1] * 8, num_heads=2)
        return len(out) == len(toks)
    if name == "vae":
        from ..vae import encoder, decoder
        img = [[[0.1 for _ in range(16)] for _ in range(16)] for _ in range(3)]
        lat = encoder.encode(img, scale=8)
        dec = decoder.decode(lat, scale=8)
        return len(dec[0]) == 16
    if name == "adapter":
        from ..adapter import reference
        img = [[[0.1 for _ in range(16)] for _ in range(16)] for _ in range(3)]
        f = reference.encode(img)
        return len(f) == 64
    if name == "prompt":
        from ..prompt import t5
        v = t5.encode_long("一只戴红围巾的柴犬" * 100)
        return len(v) == 64
    if name == "cascade":
        from ..flux.base import MockVelocity
        from ..cascade import scheduler
        p = scheduler.CascadePipeline(low_res=64, high_res=128, refine_steps=1, tiled_4k=False)
        img = p.run(MockVelocity([[[0.0] * 16 for _ in range(16)] for _ in range(4)]), [0.1] * 8)
        return len(img[0]) == 128
    if name == "edit":
        from ..edit import mask, blend
        base = [[[0.0 for _ in range(8)] for _ in range(8)] for _ in range(3)]
        m = mask.from_points(8, 8, [(4, 4)])
        out = blend.feather_blend(base, base, m)
        return len(out[0]) == 8
    if name == "engine":
        from .pipeline import GenerationPipeline
        p = GenerationPipeline()
        img = p.generate("一只柴犬", steps=2, width=64, height=64)
        return len(img[0]) == 64
    return False
