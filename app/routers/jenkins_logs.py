from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from models.user import UserResponse
from models.jenkins_log import JenkinsLogCreate, JenkinsLogResponse
from crud.jenkins_log import (
    create_jenkins_log,
    get_jenkins_log_by_id,
    get_all_jenkins_logs,
    delete_jenkins_log_by_id,
)
from utils.authentication import get_current_active_user


jenkins_log_router = APIRouter()


@jenkins_log_router.post(
    "/jenkins-logs/me",
    response_model=JenkinsLogResponse,
    tags=["jenkins-logs"],
    description="Create new parsed Jenkins log",
)
async def create_jenkins_log_router(
    jenkins_log: JenkinsLogCreate,
    current_user: Annotated[UserResponse, Depends(get_current_active_user)],
):
    jenkins_log_data = jenkins_log.model_dump()

    return await create_jenkins_log(current_user["id"], jenkins_log_data)


@jenkins_log_router.get(
    "/jenkins-logs/me/{id}",
    response_model=JenkinsLogResponse,
    tags=["jenkins-logs"],
    description="Get parsed Jenkins log by id",
)
async def get_jenkins_log_router(
    id: str, current_user: Annotated[UserResponse, Depends(get_current_active_user)]
):
    jenkins_log_in_system = await get_jenkins_log_by_id(current_user["id"], id)

    if not jenkins_log_in_system:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Parsed Jenkins log not found"
        )

    return jenkins_log_in_system


@jenkins_log_router.get(
    "/jenkins-logs/me",
    response_model=list[JenkinsLogResponse],
    tags=["jenkins-logs"],
    description="Get all parsed Jenkins logs",
)
async def get_jenkins_logs_router(
    current_user: Annotated[UserResponse, Depends(get_current_active_user)]
):
    return await get_all_jenkins_logs(current_user["id"])


@jenkins_log_router.delete(
    "/jenkins-logs/me/{id}",
    tags=["jenkins-logs"],
    description="Delete parsed Jenkins log by id",
)
async def delete_jenkins_log_router(
    id: str, current_user: Annotated[UserResponse, Depends(get_current_active_user)]
):
    if not await delete_jenkins_log_by_id(current_user["id"], id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Parsed Jenkins log not found"
        )

    return JSONResponse(
        content={"message": f"The Jenkins log with id '{id}' is deleted successfully"},
        status_code=status.HTTP_200_OK,
    )
