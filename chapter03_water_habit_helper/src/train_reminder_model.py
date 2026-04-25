"""Use the OpenAI API to estimate the chance of missing the hydration goal."""

from __future__ import annotations

import sys
from pathlib import Path
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from shared.openai_utils import clamp_score, json_completion


INPUT_PATH = ROOT / "chapter03_water_habit_helper" / "outputs" / "habit_features.csv"
OUTPUT_PATH = ROOT / "chapter03_water_habit_helper" / "outputs" / "risk_predictions.csv"
SCHEMA = {
    "type": "object",
    "properties": {
        "risk_score": {"type": "number"},
        "predicted_outcome": {"type": "string", "enum": ["likely_hit_goal", "likely_miss_goal"]},
        "main_barrier": {"type": "string"},
        "best_reminder_window": {"type": "string"},
        "confidence": {"type": "number"},
        "reasoning": {"type": "string"},
    },
    "required": ["risk_score", "predicted_outcome", "main_barrier", "best_reminder_window", "confidence", "reasoning"],
    "additionalProperties": False,
}


def predict_row(row: pd.Series) -> dict:
    prompt = (
        f"User ID: {row['user_id']}\n"
        f"Date: {row['date']}\n"
        f"Known features: {row['feature_brief']}\n"
        "Estimate whether the person is likely to miss the daily water goal. "
        "Use only the known features and do not assume the final intake."
    )
    result = json_completion(
        "You are a habit-coaching assistant. Return structured JSON for a reader-friendly teaching demo.",
        prompt,
        "hydration_risk",
        SCHEMA,
    )
    risk_score = max(0.0, min(100.0, float(result["risk_score"])))
    confidence = clamp_score(float(result["confidence"]))
    return {
        "user_id": row["user_id"],
        "date": row["date"],
        "goal_ml": row["goal_ml"],
        "actual_ml": row["actual_ml"],
        "missed_goal": row["missed_goal"],
        "risk_score": risk_score,
        "predicted_outcome": result["predicted_outcome"],
        "predicted_miss": int(result["predicted_outcome"] == "likely_miss_goal"),
        "main_barrier": result["main_barrier"],
        "best_reminder_window": result["best_reminder_window"],
        "confidence": confidence,
        "reasoning": result["reasoning"],
    }


def main() -> None:
    frame = pd.read_csv(INPUT_PATH)
    rows = [predict_row(row) for _, row in frame.iterrows()]
    pd.DataFrame(rows).to_csv(OUTPUT_PATH, index=False)
    print(f"Saved {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
