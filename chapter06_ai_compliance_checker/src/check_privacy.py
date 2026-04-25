def run_privacy_check(system_profile, checklist_items):
    findings = []
    score = 0
    for item in checklist_items:
        passed = False
        if item["id"] == "P1":
            passed = system_profile.get("collects_minimum_data", False)
        elif item["id"] == "P2":
            passed = bool(system_profile.get("retention_policy"))
        elif item["id"] == "P3":
            passed = system_profile.get("consent_flow", False)
        score += item["weight"] if passed else 0
        findings.append({"id": item["id"], "passed": passed, "question": item["question"]})
    return {"score": score, "max_score": sum(item["weight"] for item in checklist_items), "findings": findings}
