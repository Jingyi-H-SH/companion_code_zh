import json
from pathlib import Path
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = ROOT / "outputs" / "message_features.csv"
OUTPUT_PATH = ROOT / "outputs" / "topic_predictions.csv"
METRIC_PATH = ROOT / "outputs" / "topic_metrics.json"


def main() -> None:
    frame = pd.read_csv(INPUT_PATH)
    score_columns = [column for column in frame.columns if column.endswith("_score")]
    label_lookup = {column: column.replace("_score", "") for column in score_columns}

    def predict(row) -> str:
        best_column = max(score_columns, key=lambda column: row[column])
        if row[best_column] == 0:
            return "appointment_access"
        return label_lookup[best_column]

    frame["predicted_topic"] = frame.apply(predict, axis=1)
    frame["topic_match"] = frame["predicted_topic"] == frame["gold_topic"]
    accuracy = round(float(frame["topic_match"].mean()), 4)
    frame.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")
    METRIC_PATH.write_text(json.dumps({"topic_accuracy": accuracy}, indent=2), encoding="utf-8")
    print(f"主题分类准确率：{accuracy:.2%}")


if __name__ == "__main__":
    main()
