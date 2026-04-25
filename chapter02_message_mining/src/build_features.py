from pathlib import Path
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = ROOT / "outputs" / "cleaned_messages.csv"
OUTPUT_PATH = ROOT / "outputs" / "message_features.csv"

KEYWORDS = {
    "appointment_access": ["预约", "挂号", "门诊", "排队", "体检", "系统", "短信"],
    "chronic_disease": ["高血压", "糖尿病", "复诊", "血糖", "心衰", "哮喘", "头晕", "喘"],
    "diet_exercise": ["减重", "运动", "饮食", "健康", "减脂", "做饭", "少盐", "少油", "甜食"],
    "insurance_payment": ["医保", "报销", "费用", "发票", "补助", "新农合", "门诊能报"],
}


def keyword_count(text: str, keywords: list[str]) -> int:
    return sum(text.count(keyword.lower()) for keyword in keywords)


def main() -> None:
    frame = pd.read_csv(INPUT_PATH)
    for topic, keywords in KEYWORDS.items():
        frame[topic + "_score"] = frame["cleaned_text"].fillna("").map(lambda value: keyword_count(value, keywords))
    frame.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")
    print(f"已保存关键词特征表：{OUTPUT_PATH}")


if __name__ == "__main__":
    main()
