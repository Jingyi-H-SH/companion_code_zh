from pathlib import Path
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = ROOT / "outputs" / "batch_eval.csv"
OUTPUT_PATH = ROOT / "outputs" / "group_comparison.csv"


def main() -> None:
    frame = pd.read_csv(INPUT_PATH)
    summary = (
        frame.groupby(["income_level", "region"])[["response_length", "supportive_language", "referral_present"]]
        .mean()
            .reset_index()
        )
    summary.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")
    print(f"已保存分组比较结果：{OUTPUT_PATH}")


if __name__ == "__main__":
    main()
