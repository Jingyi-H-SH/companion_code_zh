"""Flag large disparities that deserve discussion in class or independent study."""

from pathlib import Path
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = ROOT / "outputs" / "group_disparities.csv"
OUTPUT_PATH = ROOT / "outputs" / "bias_flags.csv"


def severity(gap: float) -> str:
    if gap >= 0.9:
        return "high"
    if gap >= 0.5:
        return "medium"
    return "low"


def main() -> None:
    frame = pd.read_csv(INPUT_PATH)
    flagged = frame[frame["gap"] >= 0.5].copy()
    flagged["severity"] = flagged["gap"].map(severity)
    flagged["recommended_action"] = flagged.apply(
        lambda row: f"Inspect prompts and evaluation notes for {row['dimension']} because the {row['metric']} gap is {row['gap']:.2f}.",
        axis=1,
    )
    flagged.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
