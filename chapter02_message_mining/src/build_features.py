"""Create simple feature hints so beginners can inspect what the LLM sees."""

from pathlib import Path
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = ROOT / "outputs" / "cleaned_messages.csv"
OUTPUT_PATH = ROOT / "outputs" / "message_features.csv"
KEYWORDS = {
    "access": ["book", "clinic", "line", "appointment", "online"],
    "chronic": ["hypertension", "pressure", "medicine", "medication", "dizzy"],
    "lifestyle": ["diet", "exercise", "weight", "plan"],
    "payment": ["insurance", "pay", "bill", "cost"],
}


def feature_brief(text: str) -> str:
    lowered = text.lower()
    hits = {label: sum(word in lowered for word in words) for label, words in KEYWORDS.items()}
    ordered = [label for label, score in sorted(hits.items(), key=lambda item: item[1], reverse=True) if score > 0]
    labels = ", ".join(ordered) if ordered else "no strong keyword group"
    return f"Keyword hints: {labels}."


def main() -> None:
    frame = pd.read_csv(INPUT_PATH)
    frame["feature_brief"] = frame["clean_text"].map(feature_brief)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
