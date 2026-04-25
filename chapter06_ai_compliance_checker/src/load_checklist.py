"""Load the YAML checklist used by the section reviewers."""

from pathlib import Path
import yaml


ROOT = Path(__file__).resolve().parents[1]
CHECKLIST_PATH = ROOT / "data" / "policy_checklist.yaml"


def load_checklist():
    return yaml.safe_load(CHECKLIST_PATH.read_text(encoding="utf-8"))
