#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["Pillow"]
# ///
"""Web 图片优化：压缩、缩放、转 WebP"""

import sys
from pathlib import Path
from PIL import Image


def optimize(input_path: str, max_width: int = 1200, quality: int = 80):
    path = Path(input_path)
    img = Image.open(path)

    # 超过最大宽度就等比缩放
    if img.width > max_width:
        ratio = max_width / img.width
        img = img.resize((max_width, int(img.height * ratio)), Image.LANCZOS)

    # 非标准色彩模式统一转 RGB
    if img.mode not in ("RGB", "RGBA"):
        img = img.convert("RGB")

    # 保存为 WebP 并打印压缩结果
    output = path.with_suffix(".webp")
    img.save(output, "WebP", quality=quality)
    saved = (1 - output.stat().st_size / path.stat().st_size) * 100
    print(f"  {path.name} -> {output.name}, 减少 {saved:.0f}%")


if __name__ == "__main__":
    # 接收命令行参数：图片路径/目录、最大宽度、压缩质量
    target = Path(sys.argv[1])
    max_w = int(sys.argv[2]) if len(sys.argv) > 2 else 1200
    qual = int(sys.argv[3]) if len(sys.argv) > 3 else 80

    if target.is_file():
        optimize(str(target), max_w, qual)
    elif target.is_dir():
        for f in target.glob("*.png"):
            optimize(str(f), max_w, qual)
        for f in target.glob("*.jpg"):
            optimize(str(f), max_w, qual)
