"""Generate short reminder messages based on the predicted barrier."""

from __future__ import annotations

import sys
from pathlib import Path
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from shared.openai_utils import json_completion


INPUT_PATH = ROOT / "chapter03_water_habit_helper" / "outputs" / "risk_predictions.csv"
OUTPUT_PATH = ROOT / "chapter03_water_habit_helper" / "outputs" / "suggestions.csv"
SCHEMA = {
    "type": "object",
    "properties": {
        "reminder_message": {"type": "string"},
        "micro_action": {"type": "string"},
        "why_this_helps": {"type": "string"},
    },
    "required": ["reminder_message", "micro_action", "why_this_helps"],
    "additionalProperties": False,
}


def suggestion_row(row: pd.Series) -> dict:
    prompt = (
        f"User {row['user_id']} on {row['date']} has risk score {row['risk_score']}. "
        f"Main barrier: {row['main_barrier']}. Best reminder window: {row['best_reminder_window']}. "
        "Write a short English reminder, one micro-action, and one explanation line."
    )
    result = json_completion(
        "You are writing concise hydration reminders for a beginner-friendly teaching demo.",
        prompt,
        "hydration_suggestion",
        SCHEMA,
    )
    return {"user_id": row["user_id"], "date": row["date"], **result}


def main() -> None:
    frame = pd.read_csv(INPUT_PATH)
    rows = [suggestion_row(row) for _, row in frame.iterrows()]
    pd.DataFrame(rows).to_csv(OUTPUT_PATH, index=False)
    print(f"Saved {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
