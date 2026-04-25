"""Render a short markdown report from the bias audit outputs."""

from pathlib import Path
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
BATCH_PATH = ROOT / "outputs" / "batch_eval.csv"
FLAG_PATH = ROOT / "outputs" / "bias_flags.csv"
REPORT_PATH = ROOT / "outputs" / "bias_report.md"


def main() -> None:
    batch = pd.read_csv(BATCH_PATH)
    flags = pd.read_csv(FLAG_PATH)
    lines = [
        "# Bias Audit Summary",
        "",
        f"- Response rows: {len(batch)}",
        f"- Mean overall score: {batch['overall_score'].mean():.2f}",
        f"- Flagged disparities: {len(flags)}",
        "",
        "## Largest flagged gaps",
        "",
    ]
    if flags.empty:
        lines.append("- No gaps crossed the current threshold.")
    else:
        for row in flags.sort_values("gap", ascending=False).head(10).itertuples():
            lines.append(f"- `{row.dimension}` / `{row.metric}`: gap `{row.gap:.2f}` ({row.severity}). {row.recommended_action}")
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"Saved {REPORT_PATH}")


if __name__ == "__main__":
    main()
