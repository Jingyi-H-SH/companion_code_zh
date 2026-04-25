"""Ask the model for a short reader-facing reply and a moderator note."""

from __future__ import annotations

import sys
from pathlib import Path
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from shared.openai_utils import json_completion


MESSAGE_PATH = ROOT / "chapter02_message_mining" / "outputs" / "cleaned_messages.csv"
PREDICTION_PATH = ROOT / "chapter02_message_mining" / "outputs" / "message_predictions.csv"
OUTPUT_PATH = ROOT / "chapter02_message_mining" / "outputs" / "message_guidance.csv"
SCHEMA = {
    "type": "object",
    "properties": {
        "reader_reply": {"type": "string"},
        "moderator_note": {"type": "string"},
        "follow_up_question": {"type": "string"},
    },
    "required": ["reader_reply", "moderator_note", "follow_up_question"],
    "additionalProperties": False,
}


def build_guidance(row: pd.Series) -> dict:
    prompt = (
        f"Resident message: {row['raw_text']}\n"
        f"Predicted topic: {row['predicted_topic']}\n"
        f"Predicted sentiment: {row['predicted_sentiment']}\n"
        f"Urgency: {row['urgency_level']}\n"
        f"Detected need: {row['public_need']}\n"
        "Draft a short, calm English response for the reader and a one-sentence note for an instructor."
    )
    result = json_completion(
        "You write beginner-friendly public health reply guidance. Keep responses short and non-diagnostic.",
        prompt,
        "message_guidance",
        SCHEMA,
    )
    return {"message_id": row["message_id"], **result}


def main() -> None:
    messages = pd.read_csv(MESSAGE_PATH)
    predictions = pd.read_csv(PREDICTION_PATH)
    merged = messages.merge(predictions, on="message_id", how="inner")
    rows = [build_guidance(row) for _, row in merged.iterrows()]
    pd.DataFrame(rows).to_csv(OUTPUT_PATH, index=False)
    print(f"Saved {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
