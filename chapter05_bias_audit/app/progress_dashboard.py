import json
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


STATUS_COLORS = {
    "done": ("#daf5e8", "#1c8b5f"),
    "in_progress": ("#fff1cc", "#d28a00"),
    "pending": ("#eceff4", "#758195"),
}


def load_font(size, bold=False):
    candidates = []
    if bold:
        candidates.extend([
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
            "/System/Library/Fonts/Supplemental/Helvetica.ttc",
        ])
    candidates.extend([
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Helvetica.ttc",
    ])
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


def draw_card(draw, xy, fill, outline):
    draw.rounded_rectangle(xy, radius=18, fill=fill, outline=outline, width=2)


def render_dashboard(progress_path=None):
    base_dir = Path(__file__).resolve().parents[1]
    progress_path = Path(progress_path) if progress_path else base_dir / "outputs" / "progress.json"
    payload = json.loads(progress_path.read_text(encoding="utf-8"))

    width, height = 1400, 900
    image = Image.new("RGB", (width, height), "#f5f7fb")
    draw = ImageDraw.Draw(image)
    title_font = load_font(38, bold=True)
    subtitle_font = load_font(20)
    section_font = load_font(24, bold=True)
    body_font = load_font(18)
    small_font = load_font(16)

    draw.text((50, 38), payload.get("title", "Progress Dashboard"), font=title_font, fill="#14314a")
    draw.text((50, 90), payload.get("subtitle", ""), font=subtitle_font, fill="#5c6e7e")

    draw.text((50, 150), "流程进度", font=section_font, fill="#14314a")
    for index, step in enumerate(payload.get("steps", [])):
        x = 50 + (index % 2) * 660
        y = 190 + (index // 2) * 110
        fill, accent = STATUS_COLORS.get(step.get("status", "pending"), STATUS_COLORS["pending"])
        draw_card(draw, (x, y, x + 610, y + 88), "#ffffff", "#d9e0ea")
        draw.rounded_rectangle((x + 18, y + 18, x + 92, y + 70), radius=16, fill=fill, outline=accent, width=2)
        draw.text((x + 40, y + 34), str(index + 1), font=section_font, fill=accent)
        draw.text((x + 110, y + 22), step.get("name", "Step"), font=section_font, fill="#1c3247")
        draw.text((x + 110, y + 56), step.get("detail", ""), font=body_font, fill="#506274")

    draw.text((50, 560), "关键指标", font=section_font, fill="#14314a")
    metrics = payload.get("metrics", [])
    for index, metric in enumerate(metrics[:5]):
        x = 50 + index * 250
        y = 600
        draw_card(draw, (x, y, x + 220, y + 120), "#ffffff", "#d9e0ea")
        draw.text((x + 20, y + 22), metric.get("label", "Metric"), font=body_font, fill="#5f7181")
        draw.text((x + 20, y + 62), metric.get("value", "-"), font=load_font(30, bold=True), fill="#0f7b73")

    draw.text((50, 760), "读者提示", font=section_font, fill="#14314a")
    notes = payload.get("notes", [])
    for index, note in enumerate(notes[:4]):
        draw.text((70, 804 + index * 26), "• " + note, font=small_font, fill="#4e6071")

    output_path = base_dir / "outputs" / "progress_dashboard.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path)
    return output_path


if __name__ == "__main__":
    final_path = render_dashboard(sys.argv[1] if len(sys.argv) > 1 else None)
    print("进度看板已保存到 " + str(final_path))
