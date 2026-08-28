from fastapi import (
    APIRouter,
    HTTPException,
    Depends
)

from sqlalchemy.orm import Session

from app.schemas import (
    DevOpsRequest,
    AnalyzeResponse
)

from app.ai_service import (
    analyze_devops_issue
)

from app.severity_service import (
    determine_final_severity
)

from app.crud import (
    create_history_item
)

from app.dependencies import (
    get_db
)


router = APIRouter(
    prefix="/api/v1",
    tags=["Analysis"]
)


# Analyze DevOps issue
@router.post(
    "/analyze",
    response_model=AnalyzeResponse
)
def analyze_issue(
    request: DevOpsRequest,
    db: Session = Depends(get_db)
):

    try:

        # Get AI analysis
        analysis = analyze_devops_issue(
            request.issue
        )


        # Get severity returned by AI
        ai_severity = analysis.get(
            "severity",
            "Medium"
        )


        # Determine final severity
        final_severity = determine_final_severity(
            request.issue,
            ai_severity
        )


        # Ensure final severity is returned
        # consistently to frontend and database
        analysis["severity"] = final_severity


        print(
            "AI SEVERITY:",
            ai_severity
        )

        print(
            "FINAL SEVERITY:",
            final_severity
        )


        # Save analysis
        create_history_item(
            db=db,
            issue=request.issue,
            analysis=analysis
        )


        return {
            "issue_received": request.issue,
            "analysis": analysis,
            "status": "success"
        }


    except ValueError as error:

        db.rollback()

        raise HTTPException(
            status_code=422,
            detail=str(error)
        )


    except Exception as error:

        db.rollback()

        print(
            "ANALYSIS ERROR:",
            str(error)
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Something went wrong while analyzing "
                "the DevOps issue. Please try again."
            )
        )