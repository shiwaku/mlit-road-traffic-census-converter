#!/usr/bin/env python3
"""PWA 用アイコンを Pillow で生成する（SVG ラスタライザ不要）。
道路種別カラー（青・赤・緑）の斜めストロークを暗色角丸背景に配したモチーフ。"""
import os
from PIL import Image, ImageDraw

OUT = os.path.join(os.path.dirname(__file__), "..", "public", "icons")
os.makedirs(OUT, exist_ok=True)

BG = (18, 20, 27, 255)          # パネルと同じ暗色
STROKES = [
    ((0.20, 0.82), (0.62, 0.18), (76, 141, 255)),   # 青（高速）
    ((0.34, 0.86), (0.78, 0.24), (255, 77, 77)),     # 赤（一般国道）
    ((0.50, 0.90), (0.92, 0.32), (47, 179, 68)),     # 緑（主要地方道）
]


def draw_icon(size: int, *, maskable: bool) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # 背景（maskable は全面、通常は角丸）
    if maskable:
        d.rectangle([0, 0, size, size], fill=BG)
        scale, off = 0.66, 0.17     # セーフゾーン内に収める
    else:
        r = int(size * 0.22)
        d.rounded_rectangle([0, 0, size - 1, size - 1], radius=r, fill=BG)
        scale, off = 0.86, 0.07
    w = max(2, int(size * 0.085))
    for (x0, y0), (x1, y1), col in STROKES:
        p0 = (int((x0 * scale + off) * size), int((y0 * scale + off) * size))
        p1 = (int((x1 * scale + off) * size), int((y1 * scale + off) * size))
        d.line([p0, p1], fill=col + (255,), width=w)
        # 端を丸く
        for px, py in (p0, p1):
            d.ellipse([px - w // 2, py - w // 2, px + w // 2, py + w // 2], fill=col + (255,))
    return img


def save(img: Image.Image, name: str):
    img.save(os.path.join(OUT, name))
    print("wrote", name, img.size)


save(draw_icon(192, maskable=False), "icon-192.png")
save(draw_icon(512, maskable=False), "icon-512.png")
save(draw_icon(512, maskable=True), "maskable-512.png")
save(draw_icon(180, maskable=False), "apple-touch-icon.png")
save(draw_icon(32, maskable=False), "favicon-32.png")
