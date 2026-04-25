"""Create a compact chart and a small JSON summary for the chapter results."""

from pathlib import Path
import json
import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = ROOT / "outputs" / "message_predictions.csv"
SUMMARY_PATH = ROOT / "outputs" / "classification_metrics.json"
FIG_PATH = ROOT / "outputs" / "classification_overview.png"


def main() -> None:
    frame = pd.read_csv(INPUT_PATH)
    summary = {
        "messages": int(len(frame)),
        "topic_accuracy": float(frame["topic_match"].mean()),
        "mean_confidence": float(frame["confidence"].mean()),
        "high_urgency": int((frame["urgency_level"] == "high").sum()),
    }
    SUMMARY_PATH.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    topic_counts = frame["predicted_topic"].value_counts().sort_index()
    sentiment_counts = frame["predicted_sentiment"].value_counts().sort_index()

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    axes[0].bar(topic_counts.index, topic_counts.values, color="#3c8dbc")
    axes[0].tick_params(axis="x", rotation=20)
    axes[0].set_ylabel("Count")
    axes[1].bar(sentiment_counts.index, sentiment_counts.values, color="#00a65a")
    axes[1].tick_params(axis="x", rotation=20)
    axes[1].set_ylabel("Count")
    fig.tight_layout()
    fig.savefig(FIG_PATH, dpi=180)
    print(f"Saved {SUMMARY_PATH} and {FIG_PATH}")


if __name__ == "__main__":
    main()
