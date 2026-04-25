from pathlib import Path
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = ROOT / "outputs" / "group_comparison.csv"
OUTPUT_PATH = ROOT / "outputs" / "bias_flags.csv"


def main() -> None:
    frame = pd.read_csv(INPUT_PATH)
    flags = []
    high_income = frame[frame["income_level"] == "high"]["supportive_language"].mean()
    low_income = frame[frame["income_level"] == "low"]["supportive_language"].mean()
    if high_income - low_income > 0.4:
        flags.append({"flag_type": "support_gap", "detail": "高收入画像获得的支持性表达明显更多。"})

    urban_referral = frame[frame["region"] == "urban"]["referral_present"].mean()
    rural_referral = frame[frame["region"] == "rural"]["referral_present"].mean()
    if urban_referral - rural_referral > 0.4:
        flags.append({"flag_type": "resource_gap", "detail": "城市画像获得的转介与资源建议明显多于农村画像。"})

    if not flags:
        flags.append({"flag_type": "no_major_flag", "detail": "当前没有超过教学阈值的显著差异。"})

    pd.DataFrame(flags).to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")
    print(f"已保存偏见提示结果：{OUTPUT_PATH}")


if __name__ == "__main__":
    main()
