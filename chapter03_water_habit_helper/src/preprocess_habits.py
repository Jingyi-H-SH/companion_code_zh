from pathlib import Path
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = ROOT / "data" / "water_habit_log.csv"
OUTPUT_PATH = ROOT / "outputs" / "processed_habits.csv"


def main() -> None:
    frame = pd.read_csv(INPUT_PATH)
    frame["completion_rate"] = (frame["actual_ml"] / frame["goal_ml"]).round(3)
    frame["missed_goal"] = (frame["actual_ml"] < frame["goal_ml"]).astype(int)
    frame["low_morning_intake"] = (frame["intake_before_noon_ml"] < 500).astype(int)
    frame["hot_weather"] = (frame["temperature_c"] >= 30).astype(int)
    frame["high_activity"] = (frame["exercise_min"] >= 30).astype(int)
    frame["busy_flag"] = (frame["busy_day"] == "yes").astype(int)
    frame["low_sleep"] = (frame["sleep_hours"] < 7).astype(int)
    frame["row_id"] = range(1, len(frame) + 1)
    frame["is_test"] = (frame["row_id"] > int(len(frame) * 0.7)).astype(int)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")
    print(f"已保存预处理后的饮水记录：{OUTPUT_PATH}")


if __name__ == "__main__":
    main()
