from pathlib import Path
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = ROOT / "outputs" / "topic_predictions.csv"
OUTPUT_PATH = ROOT / "outputs" / "message_predictions.csv"

POSITIVE_WORDS = ["方便", "不错", "耐心", "轻松", "成功", "快"]
NEGATIVE_WORDS = ["卡住", "担心", "失败", "不清楚", "排队", "着急", "头晕", "肿了", "厉害"]
URGENT_WORDS = ["马上", "尽快", "喘得厉害", "紧急"]


def score_sentiment(text: str) -> str:
    text = str(text)
    if any(keyword in text for keyword in URGENT_WORDS):
        return "urgent"
    positive = sum(keyword in text for keyword in POSITIVE_WORDS)
    negative = sum(keyword in text for keyword in NEGATIVE_WORDS)
    if positive > negative:
        return "positive"
    if negative > positive:
        return "negative"
    return "neutral"


def main() -> None:
    frame = pd.read_csv(INPUT_PATH)
    frame["predicted_sentiment"] = frame["raw_text"].fillna("").map(score_sentiment)
    frame.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")
    print(f"已保存主题与情绪预测结果：{OUTPUT_PATH}")


if __name__ == "__main__":
    main()
