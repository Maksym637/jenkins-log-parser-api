from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from models.user import UserResponse
from models.jenkins_history import JenkinsHistoryResponse
from crud.jenkins_history import (
    get_jenkins_history_by_id,
    get_all_jenkins_histories,
    delete_jenkins_history_by_id,
)
from utils.authentication import get_current_active_user


jenkins_history_router = APIRouter()


@jenkins_history_router.get(
    "/jenkins-histories/me/{id}",
    response_model=JenkinsHistoryResponse,
    tags=["jenkins-histories"],
    description="Get Jenkins history by id",
)
async def get_jenkins_history_router(
    id: str, current_user: Annotated[UserResponse, Depends(get_current_active_user)]
):
    jenkins_history_in_system = await get_jenkins_history_by_id(current_user["id"], id)

    if not jenkins_history_in_system:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Jenkins history not found"
        )

    return jenkins_history_in_system


@jenkins_history_router.get(
    "/jenkins-histories/me",
    response_model=list[JenkinsHistoryResponse],
    tags=["jenkins-histories"],
    description="Get all Jenkins histories",
)
async def get_jenkins_histories_router(
    current_user: Annotated[UserResponse, Depends(get_current_active_user)]
):
    return await get_all_jenkins_histories(current_user["id"])


@jenkins_history_router.delete(
    "/jenkins-histories/me/{id}",
    tags=["jenkins-histories"],
    description="Delete Jenkins history by id",
)
async def delete_jenkins_history_router(
    id: str, current_user: Annotated[UserResponse, Depends(get_current_active_user)]
):
    if not await delete_jenkins_history_by_id(current_user["id"], id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Jenkins history not found"
        )

    return JSONResponse(
        content={
            "message": f"The Jenkins history with id '{id}' is deleted successfully"
        },
        status_code=status.HTTP_200_OK,
    )
