from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from models.jenkins_history import JenkinsHistoryCreate, JenkinsHistoryResponse
from utils.authentication import get_current_active_user


jenkins_history_router = APIRouter()


@jenkins_history_router.get("/jenkins-histories/me/{id}", tags=["jenkins-histories"])
async def get_jenkins_history_router():
    pass


@jenkins_history_router.get("/jenkins-histories/me", tags=["jenkins-histories"])
async def get_jenkins_histories_router():
    pass


@jenkins_history_router.delete("/jenkins-histories/me/{id}", tags=["jenkins-histories"])
async def delete_jenkins_history_router():
    pass
