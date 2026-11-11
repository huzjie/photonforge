# 常见问题

# 常见问题

## Q: import 报错

确保 `pip install -e .` 完成，或从仓库根目录运行。

## Q: 写 PNG 报错

PNG 需要 Pillow（`pip install pillow`）；或改用 PPM 输出（零依赖）。

## Q: doctor 某项 FAIL

单独运行对应子系统测试定位：`python -m unittest tests.test_xxx -v`。

