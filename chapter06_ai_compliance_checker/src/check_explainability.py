def run_explainability_check(system_profile, checklist_items):
    findings = []
    score = 0
    for item in checklist_items:
        passed = False
        if item["id"] == "E1":
            passed = system_profile.get("capability_statement", False)
        elif item["id"] == "E2":
            passed = system_profile.get("shows_reasoning_basis", False)
        elif item["id"] == "E3":
            passed = system_profile.get("human_handoff", False)
        score += item["weight"] if passed else 0
        findings.append({"id": item["id"], "passed": passed, "question": item["question"]})
    return {"score": score, "max_score": sum(item["weight"] for item in checklist_items), "findings": findings}
