import csv
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from generate_agent_reply import build_reply


SCENARIO_PATH = ROOT / "data" / "dialog_scenarios.jsonl"
OUTPUT_PATH = ROOT / "outputs" / "conversation_transcripts.csv"


def load_scenarios():
    scenarios = []
    for line in SCENARIO_PATH.read_text(encoding="utf-8").strip().splitlines():
        scenarios.append(json.loads(line))
    return scenarios


def main():
    scenarios = load_scenarios()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for scenario in scenarios:
        state = {}
        all_turns = [scenario["opening_user_message"]] + scenario["follow_up_turns"]
        for turn_id, user_text in enumerate(all_turns, start=1):
            reply, state = build_reply(user_text, state)
            rows.append(
                {
                    "scenario_id": scenario["scenario_id"],
                    "turn_id": turn_id,
                    "user_text": user_text,
                    "assistant_reply": reply,
                    "recommended_action": state.get("recommended_action", "follow_up"),
                }
            )
    with OUTPUT_PATH.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"已保存对话记录：{OUTPUT_PATH}")


if __name__ == "__main__":
    main()
