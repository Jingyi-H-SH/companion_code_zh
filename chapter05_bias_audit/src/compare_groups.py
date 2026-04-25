"""Aggregate the response quality scores across groups and save a gap chart."""

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = ROOT / "outputs" / "batch_eval.csv"
GROUP_OUTPUT = ROOT / "outputs" / "group_comparison.csv"
GAP_OUTPUT = ROOT / "outputs" / "group_disparities.csv"
FIG_PATH = ROOT / "outputs" / "group_gap_overview.png"
METRICS = ["overall_score", "empathy_score", "actionability_score", "accessibility_score", "safety_score"]
GROUP_COLUMNS = ["gender", "region", "income_level", "digital_access"]


def main() -> None:
    frame = pd.read_csv(INPUT_PATH)
    group_rows = []
    gap_rows = []
    for column in GROUP_COLUMNS:
        grouped = frame.groupby(column)[METRICS].mean().reset_index()
        grouped.insert(0, "dimension", column)
        grouped.rename(columns={column: "group"}, inplace=True)
        group_rows.append(grouped)
        for metric in METRICS:
            gap_rows.append({
                "dimension": column,
                "metric": metric,
                "gap": grouped[metric].max() - grouped[metric].min(),
            })
    comparison = pd.concat(group_rows, ignore_index=True)
    gaps = pd.DataFrame(gap_rows)
    comparison.to_csv(GROUP_OUTPUT, index=False)
    gaps.to_csv(GAP_OUTPUT, index=False)

    plot_frame = gaps[gaps["metric"] == "overall_score"]
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(plot_frame["dimension"], plot_frame["gap"], color="#dd4b39")
    ax.set_ylabel("Overall score gap")
    fig.tight_layout()
    fig.savefig(FIG_PATH, dpi=180)
    print(f"Saved {GROUP_OUTPUT}, {GAP_OUTPUT}, and {FIG_PATH}")


if __name__ == "__main__":
    main()
