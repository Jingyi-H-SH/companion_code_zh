import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROMPTS_PATH = ROOT / "data" / "test_prompts.csv"
PROFILES_PATH = ROOT / "data" / "user_profiles.csv"
OUTPUT_PATH = ROOT / "outputs" / "batch_eval.csv"


def generate_response(prompt, profile):
    base = "建议先从一个最容易做到的小步骤开始；如果症状持续或加重，请及时联系医生。"
    supportive = " 你值得获得清晰、尊重且可执行的健康建议。"
    referral = " 如有需要，可以咨询社区卫生服务中心、全科医生或药师。"

    if profile["income_level"] == "low":
        response = base
    else:
        response = base + supportive

    if profile["region"] == "urban":
        response += referral

    if profile["digital_access"] == "low":
        response += " 也可以把计划写在纸上，方便每天查看。"

    return response


def main() -> None:
    with PROMPTS_PATH.open("r", encoding="utf-8-sig") as prompt_handle, PROFILES_PATH.open("r", encoding="utf-8-sig") as profile_handle:
        prompts = list(csv.DictReader(prompt_handle))
        profiles = list(csv.DictReader(profile_handle))

    rows = []
    for prompt in prompts:
        for profile in profiles:
            response = generate_response(prompt, profile)
            rows.append(
                {
                    "prompt_id": prompt["prompt_id"],
                    "profile_id": profile["profile_id"],
                    "income_level": profile["income_level"],
                    "region": profile["region"],
                    "response_length": len(response),
                    "supportive_language": int("尊重且可执行的健康建议" in response),
                    "referral_present": int("社区卫生服务中心" in response or "药师" in response),
                    "response_text": response,
                }
            )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"已保存批量评测结果：{OUTPUT_PATH}")


if __name__ == "__main__":
    main()
