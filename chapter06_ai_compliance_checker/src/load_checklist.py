import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKLIST_PATH = ROOT / "data" / "policy_checklist.yaml"


def load_checklist():
    return json.loads(CHECKLIST_PATH.read_text(encoding="utf-8"))
