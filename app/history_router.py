import json

from fastapi import (
    APIRouter,
    HTTPException,
    Depends
)

from sqlalchemy.orm import Session

from app.dependencies import (
    get_db
)

from app.crud import (
    get_all_history,
    get_history_by_id,
    delete_history_by_id,
    clear_history,
    get_analysis_stats
)

from app.history_service import (
    format_history_item
)


router = APIRouter(
    prefix="/api/v1",
    tags=["History"]
)

@router.get("/history")
def get_history(
    db: Session = Depends(get_db)
):

    history = get_all_history(
        db
    )


    return [
        format_history_item(item)
        for item in history
    ]

@router.get("/history/{history_id}")
def get_history_item(
    history_id: int,
    db: Session = Depends(get_db)
):

    item = get_history_by_id(
        db,
        history_id
    )


    if not item:

        raise HTTPException(
            status_code=404,
            detail="History item not found."
        )


    return format_history_item(
        item
    )

@router.delete("/history/{history_id}")
def delete_history_item(
    history_id: int,
    db: Session = Depends(get_db)
):

    item = delete_history_by_id(
        db,
        history_id
    )


    if not item:

        raise HTTPException(
            status_code=404,
            detail="History item not found."
        )


    return {
        "message":
            "History item deleted successfully."
    }

@router.delete("/history")
def clear_all_history(
    db: Session = Depends(get_db)
):

    try:

        deleted_count = clear_history(
            db
        )


        return {

            "message": (
                "All analysis history "
                "deleted successfully."
            ),

            "deleted_count": deleted_count
        }


    except Exception as error:

        db.rollback()

        print(
            "CLEAR HISTORY ERROR:",
            str(error)
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to clear analysis history."
            )
        )

@router.get("/stats")
def get_stats(
    db: Session = Depends(get_db)
):

    return get_analysis_stats(
        db
    )        