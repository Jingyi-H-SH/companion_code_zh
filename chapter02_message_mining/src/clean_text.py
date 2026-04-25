"""Prepare sample resident messages for the downstream LLM workflow."""

from pathlib import Path
import re
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "sample_messages.csv"
OUTPUT_PATH = ROOT / "outputs" / "cleaned_messages.csv"


def normalize(text: str) -> str:
    text = re.sub(r"\s+", " ", text.strip())
    return text


def main() -> None:
    frame = pd.read_csv(DATA_PATH)
    frame["clean_text"] = frame["raw_text"].map(normalize)
    frame["char_count"] = frame["clean_text"].str.len()
    frame["question_marks"] = frame["clean_text"].str.count(r"\?")
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
