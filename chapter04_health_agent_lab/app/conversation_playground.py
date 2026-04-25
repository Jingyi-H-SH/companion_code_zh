"""Run the conversation scenarios and save a transcript file for review."""

from __future__ import annotations

import json
import sys
from pathlib import Path
import pandas as pd
import yaml


ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from chapter04_health_agent_lab.src.dialog_state_tracker import summarize_user_state
from chapter04_health_agent_lab.src.escalation_guard import check_escalation
from chapter04_health_agent_lab.src.generate_agent_reply import generate_reply


DATA_PATH = ROOT / "data" / "dialog_scenarios.jsonl"
POLICY_PATH = ROOT / "prompts" / "agent_policies.yaml"
OUTPUT_PATH = ROOT / "outputs" / "conversation_transcripts.csv"


def load_scenarios():
    return [json.loads(line) for line in DATA_PATH.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> None:
    scenarios = load_scenarios()
    policy = yaml.safe_load(POLICY_PATH.read_text(encoding="utf-8"))
    rows = []
    for scenario in scenarios:
        history = []
        user_turns = [scenario["opening_user_message"], *scenario.get("follow_up_turns", [])]
        for turn_index, user_message in enumerate(user_turns, start=1):
            state = summarize_user_state(user_message)
            escalation = check_escalation(user_message, policy)
            history.append(f"User: {user_message}")
            reply = generate_reply(policy, scenario["teaching_focus"], "\n".join(history), state, escalation)
            history.append(f"Assistant: {reply['assistant_reply']}")
            rows.append({
                "scenario_id": scenario["scenario_id"],
                "turn_index": turn_index,
                "speaker": "user",
                "message_text": user_message,
                "teaching_focus": scenario["teaching_focus"],
                "needs_escalation": escalation["needs_escalation"],
                "action_focus": "",
            })
            rows.append({
                "scenario_id": scenario["scenario_id"],
                "turn_index": turn_index,
                "speaker": "assistant",
                "message_text": reply["assistant_reply"],
                "teaching_focus": scenario["teaching_focus"],
                "needs_escalation": escalation["needs_escalation"],
                "action_focus": reply["action_focus"],
            })
    pd.DataFrame(rows).to_csv(OUTPUT_PATH, index=False)
    print(f"Saved {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
