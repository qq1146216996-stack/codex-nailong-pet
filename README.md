# 黄豆 · Huangdou Pet

一个始终折腰、双手捧腹大笑的黄色小伙伴。包含透明动画精灵图、九种状态、十六个视线方向，以及可本地运行的预览和导出工具。

An animated yellow companion with a continuous bent-forward belly laugh. This repository includes the transparent sprite atlas, nine animation states, sixteen gaze directions, and portable preview/export tools.

![折腰捧腹大笑](previews/laugh.gif)

## 文件

| 路径 | 内容 |
| --- | --- |
| `assets/spritesheet.png` | 最终透明 PNG，1536 × 2288，8 列 × 11 行 |
| `assets/manifest.json` | 每行状态、帧数和播放时长 |
| `preview/index.html` | 无需安装依赖的浏览器预览器 |
| `scripts/export_previews.py` | 从最终图集导出 GIF，检查帧数、透明空格和尺寸 |
| `previews/` | 大笑、全状态、视线循环、MP4 和联系表 |
| `source/idle-strip.png` | 六帧折腰大笑的原始生成动作条，洋红色抠像背景 |
| `source/prompt.md` | 角色和最终动作约束 |
| `validation/summary.json` | 最终成品的结构与质量检查摘要 |

## 预览

直接用浏览器打开 `preview/index.html`。也可以在仓库根目录运行：

```bash
python -m http.server 8000
```

然后访问 <http://localhost:8000/preview/>。播放器按图集逐帧显示，不做插帧，也不更改角色形状。

## 导出动画

```bash
python -m pip install -r requirements.txt
python scripts/export_previews.py
```

输出位于 `build/`。默认大笑循环使用 6 帧，时长为 `280, 110, 110, 140, 140, 320` 毫秒。改善流畅度靠小幅连续姿态，不是提高播放器帧率；此格式不等同于 24/60 fps 视频。

## 精灵图布局

每格 192 × 208 像素。前九行的有效帧数依次为 `6, 8, 8, 4, 5, 8, 6, 6, 6`，其余格透明。最后两行各有八个视线方向。

| 行 | 状态 | 有效帧数 |
| --- | --- | ---: |
| 0 | idle / 折腰捧腹大笑 | 6 |
| 1 | running-right / 向右跑 | 8 |
| 2 | running-left / 向左跑 | 8 |
| 3 | waving / 挥手 | 4 |
| 4 | jumping / 跳跃 | 5 |
| 5 | failed / 失落反应 | 8 |
| 6 | waiting / 等待输入 | 6 |
| 7 | running / 思考工作 | 6 |
| 8 | review / 检查结果 | 6 |
| 9 | look / 000° → 157.5° | 8 |
| 10 | look / 180° → 337.5° | 8 |

视线按顺时针排列，000° 为上、090° 为屏幕右、180° 为下、270° 为屏幕左。

导入支持这一 v2 格式的 Pets 客户端时使用 `assets/spritesheet.png`，不要上传 GIF 或原始动作条。不同客户端支持的上传格式可能不同。若桌面宠物只显示静止帧，请检查系统的“动画效果／减少动态效果”设置。

## 制作说明

角色和姿态由 OpenAI ImageGen 根据提供的形象与视频参考生成，再经确定性提取、对齐、抠像和校验组装。最终循环保持折腰、双手贴腹、眯眼张嘴，仅做小幅肩腹抖动，不在循环中站直。

这些素材是生成并筛选后的成品；提示词不保证重新生成逐像素相同的图像。本仓库不包含原始参考视频、聊天记录、账户标识、临时下载链接，或 Pets 插件内部脚本。

## 许可证

[MIT](LICENSE)。第三方参考作品不包含在仓库中；许可证仅覆盖本项目提供的贡献，不授予第三方角色或参考作品的权利。见 [NOTICE](NOTICE)。
