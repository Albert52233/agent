---
name: img-optimize
description: 优化图片用于 Web 发布：压缩体积、限制最大尺寸、转换 WebP 格式。处理图片、压缩图片、图片太大、转 WebP 时使用。
---

# 图片优化

使用脚本优化图片，支持压缩、缩放和格式转换。

优化单张图片（默认最大宽度 1200px，质量 80%）：
  uv run .agents/skills/img-optimize/scripts/optimize.py <图片路径>

批量优化目录下所有图片：
  uv run .agents/skills/img-optimize/scripts/optimize.py <目录路径>

自定义参数（最大宽度 800px，质量 60%）：
  uv run .agents/skills/img-optimize/scripts/optimize.py <路径> 800 60

输出为 WebP 格式，保存在原文件同目录。原文件不会被删除。
