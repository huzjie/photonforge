# 架构总览

# 架构总览

photonforge 把 MiniMax H3 Image 背后的技术栈拆成八个可独立使用的子系统，全部用纯 Python 标准库实现为可离线运行、可验证的参考内核。

## 分层

```
        ┌─────────────────────────────────────────┐
        │  控制面  api(FastAPI) · cli · web · sdk  │
        ├─────────────────────────────────────────┤
        │  编排    engine(流水线/批处理) · cascade  │
        ├─────────────────────────────────────────┤
        │  内核    flux · dit · vae · adapter       │
        │          prompt · edit                    │
        ├─────────────────────────────────────────┤
        │  后端    providers(mock/minimax/...)      │
        └─────────────────────────────────────────┘
```

## 设计原则

1. **零依赖内核**：flux/dit/vae/adapter/prompt/cascade/edit/engine 只依赖标准库，克隆即跑。
2. **确定性可复现**：所有随机来自 `utils.rng(key)`（md5 前 8 字节做种子），逐位可复现。
3. **多后端适配**：统一 `BaseProvider.generate/edit` 接口，mock 离线验证，真实后端填 API key 即可切换。
4. **统一交付矩阵**：CLI + FastAPI + Python/TS SDK + Web 控制台 + Docker/K8s/Helm/CI。

