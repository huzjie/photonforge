# -*- coding: utf-8 -*-
"""图像 IO：PPM 读写（零依赖）。PNG/JPEG 由可选 PIL 支持。"""
from __future__ import annotations


def tensor_to_ppm(image, path: str):
    """把 [C][H][W] 张量写入 PPM P6。"""
    c = len(image)
    h = len(image[0])
    w = len(image[0][0])
    import struct
    with open(path, "wb") as f:
        f.write(b"P6\n%d %d\n255\n" % (w, h))
        for y in range(h):
            for x in range(w):
                for cc in range(min(3, c)):
                    v = max(0, min(255, int(image[cc][y][x] * 255)))
                    f.write(struct.pack("B", v))


def ppm_to_tensor(path: str):
    """读 PPM P6 到 [C][H][W] 张量。"""
    with open(path, "rb") as f:
        magic = f.readline().strip()
        if magic not in (b"P6", b"P3"):
            raise ValueError(f"仅支持 PPM P6/P3，得到 {magic!r}")
        # 跳过注释
        line = f.readline()
        while line.startswith(b"#"):
            line = f.readline()
        w, h = map(int, line.split())
        maxval = int(f.readline().strip())
        data = f.read()
    if magic == b"P6":
        c = 3
        img = [[[0.0 for _ in range(w)] for _ in range(h)] for _ in range(c)]
        idx = 0
        for y in range(h):
            for x in range(w):
                for cc in range(c):
                    img[cc][y][x] = data[idx] / 255.0
                    idx += 1
        return img
    else:
        # P3 ASCII
        vals = list(map(int, data.split()))
        img = [[[0.0 for _ in range(w)] for _ in range(h)] for _ in range(3)]
        idx = 0
        for y in range(h):
            for x in range(w):
                for cc in range(3):
                    img[cc][y][x] = vals[idx] / max(maxval, 1)
                    idx += 1
        return img


def to_png(image, path: str):
    """写 PNG（可选 PIL）。"""
    try:
        from PIL import Image
    except ImportError as e:
        raise ImportError("写 PNG 需要 PIL（pip install pillow）或改用 PPM") from e
    c = len(image)
    h = len(image[0])
    w = len(image[0][0])
    arr = [[(0, 0, 0)] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            arr[y][x] = tuple(max(0, min(255, int(image[cc][y][x] * 255))) for cc in range(min(3, c)))
    from PIL import Image as I
    img = I.new("RGB", (w, h))
    img.putdata([arr[y][x] for y in range(h) for x in range(w)])
    img.save(path)
