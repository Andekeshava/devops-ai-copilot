from pydantic import BaseModel, Field


class DevOpsRequest(BaseModel):

    issue: str = Field(
        min_length=15,
        max_length=1000
    )


class DevOpsAnalysis(BaseModel):

    severity: str

    probable_cause: str

    what_to_check: list[str]

    commands: list[str]

    recommended_fix: list[str]


class AnalyzeResponse(BaseModel):

    issue_received: str

    analysis: DevOpsAnalysis

    status: str