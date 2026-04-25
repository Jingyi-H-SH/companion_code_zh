import json
from pathlib import Path
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = ROOT / "outputs" / "processed_habits.csv"
OUTPUT_PATH = ROOT / "outputs" / "scored_habits.csv"
MODEL_PATH = ROOT / "outputs" / "reminder_model.json"

WEIGHTS = {
    "low_morning_intake": 0.28,
    "hot_weather": 0.16,
    "high_activity": 0.16,
    "busy_flag": 0.18,
    "low_sleep": 0.10,
    "missed_previous_day": 0.12,
}


def score_row(row) -> float:
    score = 0.0
    for feature, weight in WEIGHTS.items():
        score += row[feature] * weight
    return round(score, 3)


def accuracy_at_threshold(frame, threshold):
    prediction = (frame["risk_score"] >= threshold).astype(int)
    return float((prediction == frame["missed_goal"]).mean())


def main() -> None:
    frame = pd.read_csv(INPUT_PATH)
    frame["risk_score"] = frame.apply(score_row, axis=1)
    train_frame = frame[frame["is_test"] == 0]
    candidates = [0.35, 0.4, 0.45, 0.5, 0.55]
    threshold = max(candidates, key=lambda value: accuracy_at_threshold(train_frame, value))
    frame["predicted_miss"] = (frame["risk_score"] >= threshold).astype(int)
    frame.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")
    MODEL_PATH.write_text(
        json.dumps({"weights": WEIGHTS, "threshold": threshold}, indent=2),
        encoding="utf-8",
    )
    print(f"已保存提醒模型，当前阈值为 {threshold:.2f}")


if __name__ == "__main__":
    main()
