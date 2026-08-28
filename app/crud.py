import json

from sqlalchemy.orm import Session

from app.database import AnalysisHistory


# Save analysis history
def create_history_item(
    db: Session,
    issue: str,
    analysis: dict
):

    history_item = AnalysisHistory(

        issue=issue,

        severity=analysis.get(
            "severity",
            "Medium"
        ),

        probable_cause=analysis.get(
            "probable_cause",
            ""
        ),

        what_to_check=json.dumps(
            analysis.get(
                "what_to_check",
                []
            )
        ),

        commands=json.dumps(
            analysis.get(
                "commands",
                []
            )
        ),

        recommended_fix=json.dumps(
            analysis.get(
                "recommended_fix",
                []
            )
        )
    )


    db.add(
        history_item
    )

    db.commit()

    db.refresh(
        history_item
    )


    return history_item


# Get all history
def get_all_history(
    db: Session
):

    return (

        db.query(AnalysisHistory)

        .order_by(
            AnalysisHistory.created_at.desc()
        )

        .all()

    )


# Get one history item
def get_history_by_id(
    db: Session,
    history_id: int
):

    return (

        db.query(AnalysisHistory)

        .filter(
            AnalysisHistory.id == history_id
        )

        .first()

    )


# Delete one history item
def delete_history_by_id(
    db: Session,
    history_id: int
):

    item = get_history_by_id(
        db,
        history_id
    )


    if not item:

        return None


    db.delete(
        item
    )

    db.commit()


    return item


# Clear all history
def clear_history(
    db: Session
):

    deleted_count = (

        db.query(AnalysisHistory)

        .delete()

    )


    db.commit()


    return deleted_count


# Get analysis statistics
def get_analysis_stats(
    db: Session
):

    total = (

        db.query(AnalysisHistory)

        .count()

    )


    high = (

        db.query(AnalysisHistory)

        .filter(
            AnalysisHistory.severity == "High"
        )

        .count()

    )


    medium = (

        db.query(AnalysisHistory)

        .filter(
            AnalysisHistory.severity == "Medium"
        )

        .count()

    )


    low = (

        db.query(AnalysisHistory)

        .filter(
            AnalysisHistory.severity == "Low"
        )

        .count()

    )


    return {

        "total": total,

        "high": high,

        "medium": medium,

        "low": low

    }