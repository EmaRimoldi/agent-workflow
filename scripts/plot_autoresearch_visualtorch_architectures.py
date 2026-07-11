"""Generate VisualTorch architecture diagrams for AutoResearch workloads."""

from __future__ import annotations

import sys
from pathlib import Path

import torch.nn as nn
from PIL import Image, ImageDraw, ImageFont
from visualtorch import Input
from visualtorch.flow import flow_view


ROOT = Path(__file__).resolve().parents[1]
BENCHMARK = ROOT / "autoresearch" / "benchmark" / "cifar10"
OUT = ROOT / "docs" / "assets" / "autoresearch"

sys.path.insert(0, str(BENCHMARK))

from workloads import cnn_compact, mlp_flat, resnet_micro  # noqa: E402


WORKLOADS = [
    {
        "title": "MLP",
        "subtitle": "mlp_flat · flattened image MLP · ~669k parameters",
        "module": mlp_flat,
    },
    {
        "title": "Compact CNN",
        "subtitle": "cnn_compact · two convolutional blocks · ~77k parameters",
        "module": cnn_compact,
    },
    {
        "title": "Micro ResNet",
        "subtitle": "resnet_micro · residual block with skip path · ~2.6k parameters",
        "module": resnet_micro,
    },
]

DARK_BG = (6, 10, 28)
PANEL_BG = (9, 16, 42)
TEXT = (232, 241, 255)
MUTED = (141, 162, 198)
GRID = (27, 244, 255, 34)
ACCENT_CYAN = "#18F4FF"
ACCENT_MAGENTA = "#FF2DAA"
ACCENT_VIOLET = "#9B5CFF"
ACCENT_GREEN = "#20FF9F"
ACCENT_ORANGE = "#FF9D2E"
ACCENT_YELLOW = "#FFE66D"

NEON_COLOR_MAP = {
    Input: {"fill": "#FF4D6D", "outline": "#FFD0D9"},
    nn.Conv2d: {"fill": ACCENT_CYAN, "outline": "#B7FBFF"},
    nn.Linear: {"fill": ACCENT_MAGENTA, "outline": "#FFC2E7"},
    nn.ReLU: {"fill": ACCENT_YELLOW, "outline": "#FFF7AE"},
    nn.GELU: {"fill": ACCENT_VIOLET, "outline": "#D8C6FF"},
    nn.Flatten: {"fill": ACCENT_ORANGE, "outline": "#FFD5A6"},
    nn.MaxPool2d: {"fill": ACCENT_GREEN, "outline": "#B9FFD9"},
    nn.AdaptiveAvgPool2d: {"fill": "#35D5FF", "outline": "#BDEFFF"},
    nn.Identity: {"fill": "#00E676", "outline": "#B8FFCD"},
}


def font(size: int, *, bold: bool = False) -> ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


def render_workload(module: object) -> Image.Image:
    model = module.CIFAR10Net().eval()
    image = flow_view(
        model,
        input_shape=(2, 3, 32, 32),
        draw_volume=True,
        show_dimension=True,
        spacing=32,
        padding=30,
        scale_z=0.55,
        scale_xy=2.0,
        min_xy=18,
        max_xy=280,
        min_z=12,
        max_z=130,
        type_ignore=[nn.BatchNorm1d, nn.BatchNorm2d, nn.Dropout, nn.Dropout2d],
        color_map=NEON_COLOR_MAP,
        palette="dracula",
        background_fill=DARK_BG,
        legend=True,
        font_color=TEXT,
        opacity=238,
        shade_step=18,
    )
    return image.convert("RGB")


def label_panel(title: str, subtitle: str, architecture: Image.Image, width: int) -> Image.Image:
    title_font = font(32, bold=True)
    subtitle_font = font(22)
    label_height = 96
    panel = Image.new("RGB", (width, label_height + architecture.height + 20), DARK_BG)
    draw = ImageDraw.Draw(panel)
    draw.rounded_rectangle((12, 4, width - 12, panel.height - 8), radius=24, outline=(24, 244, 255), width=2, fill=PANEL_BG)
    draw.text((34, 20), title, fill=TEXT, font=title_font)
    draw.text((34, 60), subtitle, fill=MUTED, font=subtitle_font)
    x = (width - architecture.width) // 2
    panel.paste(architecture, (x, label_height))
    return panel


def add_background_grid(draw: ImageDraw.ImageDraw, width: int, height: int) -> None:
    for x in range(0, width, 96):
        draw.line((x, 0, x, height), fill=GRID, width=1)
    for y in range(0, height, 96):
        draw.line((0, y, width, y), fill=GRID, width=1)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rendered: list[Image.Image] = []
    for workload in WORKLOADS:
        image = render_workload(workload["module"])
        image = image.resize((image.width * 3, image.height * 3), Image.Resampling.LANCZOS)
        rendered.append(image)
        image.save(OUT / f"visualtorch-{workload['title'].lower().replace(' ', '-')}.png")

    width = max(image.width for image in rendered) + 120
    panels = [
        label_panel(workload["title"], workload["subtitle"], image, width)
        for workload, image in zip(WORKLOADS, rendered)
    ]
    title_font = font(56, bold=True)
    subtitle_font = font(28)
    header_height = 146
    gap = 28
    total_height = header_height + sum(panel.height for panel in panels) + gap * (len(panels) - 1) + 44
    canvas = Image.new("RGB", (width, total_height), DARK_BG)
    draw = ImageDraw.Draw(canvas)
    add_background_grid(draw, width, total_height)
    draw.text((34, 26), "AutoResearch neural substrates", fill=TEXT, font=title_font)
    draw.text(
        (36, 92),
        "VisualTorch renderings of the small CIFAR-10 networks agents edit during the experiment.",
        fill=MUTED,
        font=subtitle_font,
    )
    y = header_height
    for panel in panels:
        canvas.paste(panel, (0, y))
        y += panel.height + gap

    canvas.save(OUT / "autoresearch-visualtorch-architectures.png")


if __name__ == "__main__":
    main()
