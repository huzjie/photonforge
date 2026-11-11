# -*- coding: utf-8 -*-
"""CLI 入口：photonforge <command>。"""
from __future__ import annotations

import argparse
import sys


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    parser = argparse.ArgumentParser(prog="photonforge",
                                     description="高速多参考图图像生成与编辑引擎")
    sub = parser.add_subparsers(dest="command", required=True)

    p_doctor = sub.add_parser("doctor", help="自检")
    p_gen = sub.add_parser("gen", help="文生图")
    p_gen.add_argument("prompt")
    p_gen.add_argument("--reference", nargs="*", default=[])
    p_gen.add_argument("--ref-weight", nargs="*", type=float, default=[])
    p_gen.add_argument("--steps", type=int, default=12)
    p_gen.add_argument("--guidance", type=float, default=4.5)
    p_gen.add_argument("--width", type=int, default=1024)
    p_gen.add_argument("--height", type=int, default=1024)
    p_gen.add_argument("--provider", default=None)
    p_gen.add_argument("--out", default="output.png")

    p_edit = sub.add_parser("edit", help="指令编辑")
    p_edit.add_argument("--instruct", required=True)
    p_edit.add_argument("--input", required=True)
    p_edit.add_argument("--out", default="edited.png")

    p_inpaint = sub.add_parser("inpaint", help="局部重绘")
    p_inpaint.add_argument("--mask", required=True)
    p_inpaint.add_argument("--input", required=True)
    p_inpaint.add_argument("--prompt", required=True)
    p_inpaint.add_argument("--out", default="fixed.png")

    p_serve = sub.add_parser("serve", help="启动服务")
    p_serve.add_argument("--host", default="127.0.0.1")
    p_serve.add_argument("--port", type=int, default=8000)

    p_bench = sub.add_parser("benchmark", help="基准测试")
    p_bench.add_argument("--prompt", default="一只柴犬")
    p_bench.add_argument("--steps", type=int, default=12)
    p_bench.add_argument("--runs", type=int, default=5)

    args = parser.parse_args(argv)

    if args.command == "doctor":
        from ..engine.doctor import run_doctor
        ok = run_doctor()
        return 0 if ok else 1
    if args.command == "gen":
        from .commands import cmd_gen
        return cmd_gen(args)
    if args.command == "edit":
        from .commands import cmd_edit
        return cmd_edit(args)
    if args.command == "inpaint":
        from .commands import cmd_inpaint
        return cmd_inpaint(args)
    if args.command == "serve":
        from .commands import cmd_serve
        return cmd_serve(args)
    if args.command == "benchmark":
        from .commands import cmd_benchmark
        return cmd_benchmark(args)
    return 1


if __name__ == "__main__":
    sys.exit(main())
