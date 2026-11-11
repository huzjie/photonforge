# DiT 主干拆解

# DiT 主干拆解

DiT（Diffusion Transformer）把潜空间图切成 patch 当 token，丢进标准 Transformer。

## 关键组件

1. **patchify**：`[C][H][W]` → `[num_patches][C*p*p]`，分辨率越高 patch 越多，容量自然扩张。
2. **adaLN**：把「时间步 + 提示词」条件投影成 scale/shift，调制每一层 LayerNorm。
3. **RoPE**：旋转位置编码，让注意力感知 patch 的空间位置。
4. **SwiGLU MLP**：门控前馈。

## 为什么能取代 U-Net

U-Net 是卷积归纳偏置，DiT 是纯注意力。DiT 的优势在于**架构与 token 数解耦**——
分辨率翻倍只增加 patch 数，不改变结构，天然适配 4K。

