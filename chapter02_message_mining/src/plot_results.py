from pathlib import Path
import pandas as pd
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = ROOT / "outputs" / "message_predictions.csv"
OUTPUT_PATH = ROOT / "outputs" / "topic_sentiment_summary.png"

TOPIC_DISPLAY = {
    "appointment_access": "预约就诊",
    "chronic_disease": "慢病管理",
    "diet_exercise": "饮食运动",
    "insurance_payment": "医保报销",
}

SENTIMENT_DISPLAY = {
    "positive": "正向",
    "negative": "负向",
    "neutral": "中性",
    "urgent": "紧急",
}


def load_font(size: int, bold: bool = False):
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
    ])
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


def draw_bar_chart(draw, origin_x, origin_y, width, height, counts, title, bar_color):
    title_font = load_font(24, bold=True)
    body_font = load_font(18)
    draw.text((origin_x, origin_y - 36), title, font=title_font, fill="#163047")
    max_value = max(counts.values())
    bar_width = width // max(len(counts), 1) - 20
    for index, (label, value) in enumerate(counts.items()):
        x0 = origin_x + index * (bar_width + 20)
        x1 = x0 + bar_width
        y1 = origin_y + height
        y0 = y1 - int((value / max_value) * (height - 40))
        draw.rounded_rectangle((x0, y0, x1, y1), radius=12, fill=bar_color, outline="#5a6c7c")
        draw.text((x0 + 12, y0 - 26), str(value), font=body_font, fill="#1f3347")
        draw.text((x0, y1 + 10), label, font=body_font, fill="#506274")


def main() -> None:
    frame = pd.read_csv(INPUT_PATH)
    topic_counts = {
        TOPIC_DISPLAY.get(label, label): count
        for label, count in frame["predicted_topic"].value_counts().sort_index().to_dict().items()
    }
    sentiment_counts = {
        SENTIMENT_DISPLAY.get(label, label): count
        for label, count in frame["predicted_sentiment"].value_counts().sort_index().to_dict().items()
    }

    image = Image.new("RGB", (1320, 720), "#f6f8fb")
    draw = ImageDraw.Draw(image)
    draw_bar_chart(draw, 70, 120, 520, 360, topic_counts, "预测主题分布", "#7db7c7")
    draw_bar_chart(draw, 700, 120, 520, 360, sentiment_counts, "规则情绪分布", "#88b88f")
    image.save(OUTPUT_PATH)
    print(f"已保存统计图：{OUTPUT_PATH}")


if __name__ == "__main__":
    main()
