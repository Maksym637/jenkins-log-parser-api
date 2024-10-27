from pydantic import BaseModel


class JenkinsHistoryCreateComplete(BaseModel):
    time_executed: str
    time_spent: float
    jenkins_log_id: str
    user_id: str


class JenkinsHistoryResponse(BaseModel):
    id: str
    time_executed: str
    time_spent: float
    jenkins_log_id: str
    user_id: str
