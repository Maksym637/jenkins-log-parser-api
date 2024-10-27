from pydantic import BaseModel
from datetime import datetime


class JenkinsHistoryCreate(BaseModel):
    time_executed: datetime
    time_spent: str
    jenkins_log_id: str
    user_id: str


class JenkinsHistoryResponse(BaseModel):
    id: str
    time_executed: datetime
    time_spent: str
    jenkins_log_id: str
    user_id: str
