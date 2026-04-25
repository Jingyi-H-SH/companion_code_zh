import json
from pathlib import Path
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = ROOT / "outputs" / "scored_habits.csv"
OUTPUT_PATH = ROOT / "outputs" / "evaluation.json"


def ratio(numerator, denominator):
    return round(numerator / denominator, 4) if denominator else 0.0


def main() -> None:
    frame = pd.read_csv(INPUT_PATH)
    test_frame = frame[frame["is_test"] == 1]
    tp = int(((test_frame["predicted_miss"] == 1) & (test_frame["missed_goal"] == 1)).sum())
    tn = int(((test_frame["predicted_miss"] == 0) & (test_frame["missed_goal"] == 0)).sum())
    fp = int(((test_frame["predicted_miss"] == 1) & (test_frame["missed_goal"] == 0)).sum())
    fn = int(((test_frame["predicted_miss"] == 0) & (test_frame["missed_goal"] == 1)).sum())
    metrics = {
        "accuracy": ratio(tp + tn, len(test_frame)),
        "precision": ratio(tp, tp + fp),
        "recall": ratio(tp, tp + fn),
        "test_rows": int(len(test_frame)),
    }
    OUTPUT_PATH.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(json.dumps(metrics, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
