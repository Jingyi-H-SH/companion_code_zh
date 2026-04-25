from pathlib import Path
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = ROOT / "outputs" / "scored_habits.csv"
OUTPUT_PATH = ROOT / "outputs" / "suggestions.csv"


def build_suggestion(row) -> str:
    tips = []
    if row["low_morning_intake"]:
        tips.append("可以设置 10:30 提醒，尽量在上午喝完第一瓶水")
    if row["hot_weather"]:
        tips.append("天气较热，建议下午额外准备约 400 毫升饮水")
    if row["high_activity"]:
        tips.append("运动前和运动后各补一次水，更容易达到目标")
    if row["busy_flag"]:
        tips.append("可以把喝水和日程切换绑定，减少忙碌时忘记喝水")
    if row["low_sleep"]:
        tips.append("睡眠不足时更容易忽略补水，建议把水杯直接放在桌面显眼位置")
    if row["missed_previous_day"]:
        tips.append("如果昨天没达标，今天可以先设一个午饭前的小补水目标")
    if not tips:
        tips.append("当前习惯比较稳定，可以继续保持，并在午后再检查一次进度")
    return "；".join(tips)


def main() -> None:
    frame = pd.read_csv(INPUT_PATH)
    high_risk = frame[(frame["is_test"] == 1) & (frame["predicted_miss"] == 1)].copy()
    high_risk["suggestion"] = high_risk.apply(build_suggestion, axis=1)
    high_risk[["user_id", "date", "risk_score", "suggestion"]].to_csv(
        OUTPUT_PATH,
        index=False,
        encoding="utf-8-sig",
    )
    print(f"已保存个性化提醒建议：{OUTPUT_PATH}")


if __name__ == "__main__":
    main()
