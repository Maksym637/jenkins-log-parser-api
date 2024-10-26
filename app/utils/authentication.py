import base64
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from models.user import UserResponse
from crud.user import get_user_by_username


security = HTTPBasic()


async def get_current_user(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    user = await get_user_by_username(credentials.username)
    if not user or not is_credentials(user, credentials.username, credentials.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user


async def get_current_active_user(
    current_user: Annotated[UserResponse, Depends(get_current_user)]
):
    if not current_user["is_active"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User is inactive"
        )
    return current_user


def is_credentials(user, username: str, password: str) -> bool:
    if user:
        return user["hashed_credentials"] == create_bearer_token(username, password)
    return False


def create_bearer_token(username: str, password: str) -> str:
    message = f"{username}:{password}"
    message_bytes = message.encode("ascii")

    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode("ascii")

    return base64_message
