# photonforge · 高速多参考图图像生成与编辑引擎

> 面向「开源 SOTA 级高速文生图」的一站式**生成、编辑、多参考图融合与分布式部署**平台。
> 以 2026-11-11 MiniMax 开源 **H3 Image**（4K 出图 10–20 秒、最多 16 张参考图、7500 字符提示词、开源 SOTA）为技术蓝本，
> 把「Rectified Flow 少步采样、DiT 主干、VAE 潜空间、IP-Adapter 多参考图注入、长提示词编码、级联 4K 分辨率」这套方法论，
> 工程化成一个**零依赖、可离线运行、可复现**的开源引擎。

---

## 这是什么

photonforge 不是一个「模型」，而是一套**围绕高速文生图与多参考图编辑的生成运行时**。它把 H3 Image 背后的关键技术拆成八个可独立使用的子系统，全部用**纯 Python 标准库**实现为可离线运行、可验证的参考内核：

| 子系统 | 解决的问题 | 对应 H3 Image 技术点 |
|---|---|---|
| `flux` | 为什么 10–20 秒就能出一张 4K 图 | Rectified Flow 直线路径 + 少步采样（8~20 步）+ CFG |
| `dit` | 图像怎么用 Transformer 建模 | DiT 主干：patchify + adaLN + 全注意力 + RoPE |
| `vae` | 4K 图怎么不逐像素算 | VAE 8x 潜空间编解码（KL + VQ） |
| `adapter` | 最多 16 张参考图怎么融进生成 | IP-Adapter 解耦交叉注意力 + 多参考图加权融合 |
| `prompt` | 7500 字符长提示词怎么吃进去 | T5/CLIP 双编码 + 分块 + 提示词加权 |
| `cascade` | 4K 分辨率怎么「够快又够清」 | 低分辨率潜空间生成 → 高分辨率细化（级联） |
| `edit` | 怎么指令式改图、局部重绘、外扩 | instruct-edit + inpaint + outpaint + 蒙版融合 |
| `engine` | 怎么对外提供生产级生成服务 | 采样编排 + 连续批处理 + 多 Provider 适配 + Web 控制台 |

每个子系统都带**离线可跑**的参考实现（`mock` / 纯标准库内核），接上真实后端（MiniMax API / diffusers / ComfyUI / A1111 / OpenAI 图像兼容）即可直接对外服务。

---

## 为什么值得看（技术原理速览）

**1. 为什么「10–20 秒出一张 4K」？核心是 Rectified Flow。**
传统 DDPM 走的是「噪声 → 图像」的随机弯曲路径，需要 50–1000 步。Rectified Flow 把这条路径**拉直**成「噪声到图像的直线」，训练目标变成拟合一个恒定速度场 `v = x_1 - x_0`，采样时沿着直线一次就能走很远——于是 8~20 步即可出图，步数直接决定出图速度。`flux/` 完整实现了 flow 轨迹构造、少步 Euler/Heun/DPM-Solver 采样与 CFG 引导。

**2. DiT 为什么能取代 U-Net？**
DiT 把潜空间图切成 patch 当 token，丢进标准 Transformer，用 **adaLN（自适应层归一化）** 把「时间步 + 提示词」作为条件调制进每一层（缩放 + 平移），配合 RoPE 位置编码。好处是：架构与 token 数解耦，分辨率越高 patch 越多、模型容量自然扩张，天然适配 4K。`dit/` 实现了 patchify、adaLN、全注意力、RoPE、前馈 MLP 的完整链路。

**3. VAE 为什么能「4K 不逐像素」？**
4K = 4096×4096 ≈ 1677 万像素。若直接逐像素扩散，计算量爆炸。VAE 先做 8x 下采样（→ 512×512 潜空间），在潜空间做扩散，最后 decode 回 4K。`vae/` 实现了 KL 正则编码 + VQ 码本量化两套潜空间。

**4. 16 张参考图怎么「一次性融进生成」？**
IP-Adapter 的「解耦交叉注意力」把参考图特征作为**独立的键值（K/V）**注入，与文本交叉注意力并行，用权重系数控制参考图影响强度——所以参考图可以是「风格图」「人脸图」「构图图」，能任意组合、任意加权。`adapter/` 实现了参考图编码、解耦注意力、多参考图加权融合与风格/人脸/构图三类注入模式。

**5. 7500 字符长提示词怎么处理？**
文本编码器有长度上限（T5 通常 512 token）。长提示词需要**分块编码 + 注意力池化**，再把分段语义聚合成一个全局条件向量。`prompt/` 实现了 T5 风格分块、CLIP 风格对比编码、提示词权重解析（`(词:1.3)` 语法）与长提示词分段。

---

## 快速开始

```bash
git clone https://github.com/huzjie/photonforge.git
cd photonforge
pip install -e .            # 零第三方依赖即可跑内核；[api] 安装 FastAPI 控制面

photonforge doctor          # 自检：八个子系统逐项诊断
photonforge gen "一只戴红围巾的柴犬，冬日清晨，柔和逆光，4k，电影感" --provider mock --steps 8
photonforge gen --reference style.jpg face.jpg --ref-weight 0.7 0.4 --out dog_4k.png
photonforge edit --instruct "把背景换成雪地" --input photo.png --out edited.png
photonforge inpaint --mask mask.png --input photo.png --prompt "修复脸部" --out fixed.png
photonforge serve --port 8000                            # REST API + Web 控制台
```

接真实后端（示例接 MiniMax H3 Image API）：

```bash
export PF_PROVIDER=minimax PF_API_KEY=<your-key> PF_MODEL=h3-image
photonforge gen "蒸汽朋克城市夜景，赛博霓虹，4k" --out city.png
```

---

## 仓库结构（200+ 文件）

```
photonforge/
├── photonforge/           # 核心包（纯标准库内核 + 可选 FastAPI 控制面）
│   ├── flux/              # Rectified Flow 轨迹 + 少步采样器 + CFG
│   ├── dit/               # DiT 主干：patchify/adaLN/注意力/RoPE/MLP
│   ├── vae/               # 潜空间编解码（KL + VQ）
│   ├── adapter/           # IP-Adapter 多参考图注入
│   ├── prompt/            # T5/CLIP 长提示词编码
│   ├── cascade/           # 级联分辨率 4K 细化
│   ├── edit/              # instruct-edit / inpaint / outpaint
│   ├── engine/            # 采样编排 + 连续批处理
│   ├── providers/         # mock/minimax/diffusers/comfyui/a1111/openai
│   ├── tools/             # 图像 IO / 缩放 / 裁剪 / 提示词模板
│   ├── api/               # FastAPI 控制面
│   ├── cli/               # doctor/gen/edit/inpaint/serve/benchmark
│   ├── sdk/               # Python / TypeScript 客户端
│   └── web/               # Web 控制台
├── deploy/                # k8s · Helm（含 GPU 分片配置）
├── docs/                  # 25+ 篇技术文档
├── prompts/               # 提示词模板
├── recipes/               # 配方（风格/构图/编辑）
├── examples/              # 可运行示例
├── tests/                 # 单测（纯标准库 unittest）
├── .github/workflows/     # CI / Release / CodeQL
├── Dockerfile             # 多阶段构建
└── config.example.yaml    # 全量配置模板
```

---

## 许可证

MIT License。参见 [LICENSE](LICENSE)。

> 说明：本项目为**独立开源实现**，与 MiniMax 无隶属关系；`minimax` provider 仅为对接其公开 API 的适配器。
