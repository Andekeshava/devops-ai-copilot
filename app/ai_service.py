import boto3
import json


def normalize_severity(severity):

    severity = str(
        severity
    ).strip().lower()


    if severity in [
        "critical",
        "high",
        "severe",
        "urgent"
    ]:

        return "High"


    if severity in [
        "medium",
        "moderate",
        "warning"
    ]:

        return "Medium"


    return "Low"


def validate_analysis(analysis):

    if not isinstance(
        analysis,
        dict
    ):

        raise ValueError(
            "AI returned an invalid analysis format."
        )


    probable_cause = analysis.get(
        "probable_cause",
        ""
    )


    what_to_check = analysis.get(
        "what_to_check",
        []
    )


    commands = analysis.get(
        "commands",
        []
    )


    recommended_fix = analysis.get(
        "recommended_fix",
        []
    )


    # Convert invalid values safely
    if not isinstance(
        what_to_check,
        list
    ):

        what_to_check = []


    if not isinstance(
        commands,
        list
    ):

        commands = []


    if not isinstance(
        recommended_fix,
        list
    ):

        recommended_fix = []


    return {

        "severity": normalize_severity(
            analysis.get(
                "severity",
                "Low"
            )
        ),

        "probable_cause": str(
            probable_cause
        ).strip() or (
            "Unable to determine the probable "
            "cause from the available information."
        ),

        "what_to_check": [
            str(item)
            for item in what_to_check
        ],

        "commands": [
            str(item)
            for item in commands
        ],

        "recommended_fix": [
            str(item)
            for item in recommended_fix
        ]
    }


def analyze_devops_issue(issue: str):

    session = boto3.Session(
        profile_name="new-aws-account",
        region_name="ap-south-1"
    )


    bedrock_client = session.client(
        "bedrock-runtime"
    )


    response = bedrock_client.converse(

        modelId="apac.amazon.nova-lite-v1:0",

        messages=[
            {
                "role": "user",

                "content": [
                    {
                        "text": f"""
You are an expert DevOps and Cloud troubleshooting assistant.

Analyze the DevOps issue provided by the user.

Return ONLY valid JSON.
Do not use Markdown.
Do not use ```json.
Do not include any explanation outside the JSON.

Use exactly this structure:

{{
    "severity": "High | Medium | Low",
    "probable_cause": "string",
    "what_to_check": [
        "string",
        "string"
    ],
    "commands": [
        "string",
        "string"
    ],
    "recommended_fix": [
        "string",
        "string"
    ]
}}

SEVERITY RULES:

High:
- Production application completely down
- Service unavailable
- Major outage
- Critical security issue
- Data loss
- Users cannot access a production service

Medium:
- Deployment failures
- CI/CD failures
- Kubernetes pod failures
- Infrastructure issues affecting functionality
- Authentication or permission problems

Low:
- Warnings
- Non-critical dependency issues
- Minor configuration issues
- Informational problems
- No immediate service impact

COMMAND RULES:

1. Every command must be syntactically complete.
2. Never return incomplete commands.
3. Never leave flags without values.
4. Use clear placeholders when actual values are unknown.
5. Do not invent actual account IDs, credentials, resource names, or pod names.
6. Use placeholders such as <region>, <account-id>, <pod-name>, and <namespace>.
7. Prefer safe diagnostic commands first.
8. Keep the response concise and practical.

DevOps issue:

{issue}
"""
                    }
                ]
            }
        ],

        inferenceConfig={
            "maxTokens": 800,
            "temperature": 0.2
        }
    )


    ai_response = (
        response["output"]
        ["message"]
        ["content"][0]
        ["text"]
    )


    # Remove accidental Markdown code blocks
    ai_response = ai_response.strip()


    if ai_response.startswith(
        "```json"
    ):

        ai_response = ai_response[7:]


    elif ai_response.startswith(
        "```"
    ):

        ai_response = ai_response[3:]


    if ai_response.endswith(
        "```"
    ):

        ai_response = ai_response[:-3]


    ai_response = ai_response.strip()


    try:

        analysis = json.loads(
            ai_response
        )


    except json.JSONDecodeError:

        raise ValueError(
            "Unable to generate a valid AI analysis. "
            "Please try again."
        )


    # Validate and normalize AI response
    return validate_analysis(
        analysis
    )