from pathlib import Path
import pandas as pd
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
COMPARE_PATH = ROOT / "outputs" / "group_comparison.csv"
FLAG_PATH = ROOT / "outputs" / "bias_flags.csv"
IMAGE_PATH = ROOT / "outputs" / "bias_report.png"
MARKDOWN_PATH = ROOT / "outputs" / "bias_report.md"

INCOME_DISPLAY = {"low": "低收入", "middle": "中等收入", "high": "高收入"}
REGION_DISPLAY = {"urban": "城市", "rural": "农村"}


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


def main() -> None:
    comparison = pd.read_csv(COMPARE_PATH)
    flags = pd.read_csv(FLAG_PATH)
    report_lines = [
        "# 偏见检测报告",
        "",
        "## 分组比较",
        comparison.to_string(index=False),
        "",
        "## 偏见提示",
        flags.to_string(index=False),
    ]
    MARKDOWN_PATH.write_text("\n".join(report_lines), encoding="utf-8")

    image = Image.new("RGB", (1280, 760), "#f7f9fc")
    draw = ImageDraw.Draw(image)
    title_font = load_font(34, bold=True)
    body_font = load_font(18)
    draw.text((50, 40), "偏见检测摘要", font=title_font, fill="#12324a")
    draw.text((50, 100), "关键分组均值", font=load_font(24, bold=True), fill="#12324a")
    y = 150
    for _, row in comparison.iterrows():
        income = INCOME_DISPLAY.get(row["income_level"], row["income_level"])
        region = REGION_DISPLAY.get(row["region"], row["region"])
        text = f"{income} / {region} -> 回答长度 {row['response_length']:.1f}，支持性表达 {row['supportive_language']:.2f}，转介建议 {row['referral_present']:.2f}"
        draw.text((70, y), text, font=body_font, fill="#4b5e70")
        y += 34
    draw.text((50, 430), "警示摘要", font=load_font(24, bold=True), fill="#12324a")
    y = 480
    for _, row in flags.iterrows():
        draw.text((70, y), f"- {row['flag_type']}: {row['detail']}", font=body_font, fill="#9b2f2f")
        y += 34
    image.save(IMAGE_PATH)
    print(f"已保存偏见检测报告：{IMAGE_PATH}")


if __name__ == "__main__":
    main()
