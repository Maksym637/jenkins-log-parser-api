from pydantic import BaseModel
from typing import List


class JenkinsLogCreate(BaseModel):
    external_url: str


class ParsedLogData(BaseModel):
    test_name: str
    test_result: str
    test_reason: str


class ChartLogData(BaseModel):
    passed: int
    failed: int
    errored: int
    skipped: int
    blocked: int


class JenkinsLogCreateComplete(BaseModel):
    parsed_log_data: List[ParsedLogData]
    chart_log_data: ChartLogData
    user_id: str


class JenkinsLogResponse(BaseModel):
    id: str
    parsed_log_data: List[ParsedLogData]
    chart_log_data: ChartLogData
    user_id: str
