# 内容安全

# 内容安全

- `safety/filter.py`：提示词敏感词拦截（blocklist + sanitize）。
- `safety/nsfw.py`：NSFW 检测占位，接真实分类器。
- `safety/watermark.py`：LSB 隐形水印，可溯源。

## 可复用思路

生成系统上线前必须加内容安全层：提示词侧拦截 + 输出侧检测 + 隐形水印溯源，
三层缺一不可。

