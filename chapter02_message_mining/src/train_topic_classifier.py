"""Use the OpenAI API to classify topics and sentiments for each message."""

from __future__ import annotations

import sys
from pathlib import Path
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from shared.openai_utils import clamp_score, json_completion


INPUT_PATH = ROOT / "chapter02_message_mining" / "outputs" / "message_features.csv"
OUTPUT_PATH = ROOT / "chapter02_message_mining" / "outputs" / "message_predictions.csv"
TOPICS = ["appointment_access", "chronic_disease", "diet_exercise", "insurance_payment"]
SCHEMA = {
    "type": "object",
    "properties": {
        "predicted_topic": {"type": "string", "enum": TOPICS},
        "predicted_sentiment": {"type": "string", "enum": ["informational", "concerned", "frustrated", "urgent"]},
        "urgency_level": {"type": "string", "enum": ["low", "moderate", "high"]},
        "confidence": {"type": "number"},
        "reasoning": {"type": "string"},
        "public_need": {"type": "string"},
    },
    "required": ["predicted_topic", "predicted_sentiment", "urgency_level", "confidence", "reasoning", "public_need"],
    "additionalProperties": False,
}
SYSTEM_PROMPT = (
    "You are helping a beginner health communication class. "
    "Read a short resident message and assign one topic and one sentiment label. "
    "Use the provided feature brief only as a hint, and keep the reasoning concise."
)


def classify_row(row: pd.Series) -> dict:
    user_prompt = (
        f"Message ID: {row['message_id']}\n"
        f"Original text: {row['raw_text']}\n"
        f"Normalized text: {row['clean_text']}\n"
        f"Feature brief: {row['feature_brief']}\n"
        f"Available topics: {', '.join(TOPICS)}\n"
        "Return JSON only."
    )
    result = json_completion(SYSTEM_PROMPT, user_prompt, "message_classification", SCHEMA)
    return {
        "message_id": row["message_id"],
        "gold_topic": row["gold_topic"],
        "predicted_topic": result["predicted_topic"],
        "topic_match": result["predicted_topic"] == row["gold_topic"],
        "predicted_sentiment": result["predicted_sentiment"],
        "urgency_level": result["urgency_level"],
        "confidence": clamp_score(float(result["confidence"])),
        "reasoning": result["reasoning"],
        "public_need": result["public_need"],
    }


def main() -> None:
    frame = pd.read_csv(INPUT_PATH)
    results = [classify_row(row) for _, row in frame.iterrows()]
    pd.DataFrame(results).to_csv(OUTPUT_PATH, index=False)
    print(f"Saved {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
