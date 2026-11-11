# Provider 适配

# Provider 适配

| Provider | 类型 | 依赖 |
|---|---|---|
| mock | 离线确定性 | 无 |
| minimax | MiniMax H3 Image API | api_key |
| diffusers | HF diffusers | torch |
| comfyui | ComfyUI 工作流 | 本地服务 |
| a1111 | SD WebUI | 本地服务 |
| openai | OpenAI 图像 API | api_key |

统一接口 `generate(prompt, reference_images, ...)` / `edit(instruction, image)`。

