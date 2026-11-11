# ControlNet 结构化控制

# ControlNet 结构化控制

- `controlnet/canny.py`：Canny 边缘检测（sobel 算子）。
- `controlnet/depth.py`：深度估计占位（接 MiDaS）。
- `controlnet/pose.py`：姿态控制占位（接 OpenPose）。

## 可复用思路

纯文生图不可控时，加结构化条件（边缘/深度/姿态）能让构图可控。

