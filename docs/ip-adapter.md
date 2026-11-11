# IP-Adapter 多参考图注入

# IP-Adapter：16 张参考图怎么融进生成

## 解耦交叉注意力

IP-Adapter 把参考图特征作为**独立的 K/V** 注入，与文本交叉注意力并行：

```
out = text_attention(Q, K_text, V_text) + scale * ref_attention(Q, K_ref, V_ref)
```

参考图可与文本提示词任意组合、任意加权。

## 三种注入模式

- **style**：强调全局风格，取特征均值。
- **face**：强调局部一致，保留高频（差分）。
- **composition**：强调空间布局，保留网格顺序。
- **mixed**：混合风格与构图。

## 权重策略

多参考图权重可显式指定（如 `[0.7, 0.4]`），也可 softmax 归一、等权。
`adapter/weighting.py` 提供三种归一化。

