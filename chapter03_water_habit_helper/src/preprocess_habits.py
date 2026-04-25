"""Transform the habit log into interpretable fields for LLM-based risk estimation."""

from pathlib import Path
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "water_habit_log.csv"
OUTPUT_PATH = ROOT / "outputs" / "habit_features.csv"


def main() -> None:
    frame = pd.read_csv(DATA_PATH)
    frame["missed_goal"] = (frame["actual_ml"] < frame["goal_ml"]).astype(int)
    frame["morning_progress_ratio"] = (frame["intake_before_noon_ml"] / frame["goal_ml"]).round(2)
    frame["busy_binary"] = frame["busy_day"].map({"yes": 1, "no": 0}).fillna(0).astype(int)
    frame["feature_brief"] = frame.apply(
        lambda row: (
            f"Goal {row['goal_ml']} ml; noon intake {row['intake_before_noon_ml']} ml; "
            f"temperature {row['temperature_c']}C; exercise {row['exercise_min']} min; "
            f"busy day {row['busy_day']}; sleep {row['sleep_hours']} h; "
            f"missed previous day {row['missed_previous_day']}."
        ),
        axis=1,
    )
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
