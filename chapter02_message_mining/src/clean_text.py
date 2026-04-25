import re
from pathlib import Path
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = ROOT / "data" / "sample_messages.csv"
OUTPUT_PATH = ROOT / "outputs" / "cleaned_messages.csv"


def normalize_text(text: str) -> str:
    text = str(text).strip()
    text = re.sub(r'[，。！？；：,.!?;:（）()【】\[\]“”‘’"]', " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip().lower()


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    frame = pd.read_csv(INPUT_PATH)
    frame["cleaned_text"] = frame["raw_text"].fillna("").map(normalize_text)
    frame.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")
    print(f"已保存清洗后的留言数据：{OUTPUT_PATH}")


if __name__ == "__main__":
    main()
