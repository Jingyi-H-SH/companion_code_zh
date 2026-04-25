def run_fairness_check(system_profile, checklist_items):
    findings = []
    score = 0
    for item in checklist_items:
        passed = False
        if item["id"] == "F1":
            passed = system_profile.get("group_testing_complete", False)
        elif item["id"] == "F2":
            passed = system_profile.get("post_deployment_monitoring", False)
        elif item["id"] == "F3":
            passed = system_profile.get("appeal_path", False)
        score += item["weight"] if passed else 0
        findings.append({"id": item["id"], "passed": passed, "question": item["question"]})
    return {"score": score, "max_score": sum(item["weight"] for item in checklist_items), "findings": findings}
