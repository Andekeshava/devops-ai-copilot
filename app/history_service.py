import json


def format_history_item(item):

    return {

        "id": item.id,

        "issue": item.issue,

        "severity": item.severity,

        "created_at":
            item.created_at.isoformat(),

        "analysis": {

            "severity": item.severity,

            "probable_cause":
                item.probable_cause,

            "what_to_check":
                json.loads(
                    item.what_to_check
                ),

            "commands":
                json.loads(
                    item.commands
                ),

            "recommended_fix":
                json.loads(
                    item.recommended_fix
                )
        }
    }