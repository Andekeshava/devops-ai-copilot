from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.dependencies import (
    get_db
)

from app.crud import (
    get_analysis_stats
)


router = APIRouter(
    prefix="/api/v1",
    tags=["Statistics"]
)


@router.get("/stats")
def get_stats(
    db: Session = Depends(get_db)
):

    return get_analysis_stats(
        db
    )