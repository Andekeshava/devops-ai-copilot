# Normalize severity
def normalize_severity(severity: str):

    if not severity:
        return "Medium"

    severity = severity.strip().lower()

    if severity == "high":
        return "High"

    if severity == "medium":
        return "Medium"

    if severity == "low":
        return "Low"

    return "Medium"


# Apply severity rules
def determine_final_severity(
    issue: str,
    ai_severity: str
):

    issue_text = issue.lower()


    # HIGH severity keywords
    high_keywords = [

        "production application is completely down",
        "production is down",
        "application is completely down",
        "service is completely down",
        "users cannot access",
        "service unavailable",
        "service is unavailable",
        "production outage",
        "critical outage",
        "major outage",
        "entire application down",
        "all users cannot access",
        "data loss",
        "security breach",
        "ransomware"
    ]


    # LOW severity keywords
    low_keywords = [

        "non-critical warning",
        "minor warning",
        "cosmetic issue",
        "informational",
        "information message",
        "deprecated warning",
        "outdated dependency warning",
        "minor issue"
    ]


    # Check HIGH severity first
    for keyword in high_keywords:

        if keyword in issue_text:

            return "High"


    # Check LOW severity
    for keyword in low_keywords:

        if keyword in issue_text:

            return "Low"


    # Otherwise use AI severity
    return normalize_severity(
        ai_severity
    )