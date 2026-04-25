"""Evaluate the LLM risk predictions and save a simple chart."""

from pathlib import Path
import json
import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = ROOT / "outputs" / "risk_predictions.csv"
EVAL_PATH = ROOT / "outputs" / "evaluation.json"
FIG_PATH = ROOT / "outputs" / "risk_vs_actual.png"


def main() -> None:
    frame = pd.read_csv(INPUT_PATH)
    tp = int(((frame["predicted_miss"] == 1) & (frame["missed_goal"] == 1)).sum())
    tn = int(((frame["predicted_miss"] == 0) & (frame["missed_goal"] == 0)).sum())
    fp = int(((frame["predicted_miss"] == 1) & (frame["missed_goal"] == 0)).sum())
    fn = int(((frame["predicted_miss"] == 0) & (frame["missed_goal"] == 1)).sum())
    accuracy = (tp + tn) / len(frame)
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    evaluation = {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "predicted_miss_days": int(frame["predicted_miss"].sum()),
        "suggestion_rows": int(len(frame)),
    }
    EVAL_PATH.write_text(json.dumps(evaluation, ensure_ascii=False, indent=2), encoding="utf-8")

    grouped = frame.groupby("user_id")[["risk_score", "missed_goal"]].mean().reset_index()
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(grouped["user_id"], grouped["risk_score"], color="#00a7d0", alpha=0.8, label="Risk score")
    ax.plot(grouped["user_id"], grouped["missed_goal"] * 100, color="#f39c12", marker="o", label="Miss rate (%)")
    ax.set_ylabel("Score / Percent")
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIG_PATH, dpi=180)
    print(f"Saved {EVAL_PATH} and {FIG_PATH}")


if __name__ == "__main__":
    main()
