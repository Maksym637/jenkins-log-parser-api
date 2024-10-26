from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from models.user import UserLogin, UserCreate, UserResponse
from crud.user import (
    create_user,
    get_user_by_id,
    get_user_by_username,
    get_all_users,
    update_user,
    delete_user,
)
from utils.authentication import (
    get_current_active_user,
    is_credentials,
    create_bearer_token,
)


user_router = APIRouter()


@user_router.post("/user", response_model=UserResponse)
async def create_user_router(user: UserCreate):
    user_data = user.model_dump(exclude={"password"})
    user_data["hashed_credentials"] = create_bearer_token(user.username, user.password)
    return await create_user(user_data)


@user_router.post("/login")
async def login_router(user: UserLogin):
    user_data = await get_user_by_username(user.username)

    if not user_data or not is_credentials(user_data, user.username, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    token = create_bearer_token(user.username, user.password)

    return {"access_token": token, "token_type": "bearer"}


@user_router.post("/logout")
async def logout_router(
    current_user: Annotated[UserResponse, Depends(get_current_active_user)]
):
    return {"message": "Logged out successfully"}


@user_router.get("/user/{id}", response_model=UserResponse)
async def get_user_router(
    id: str, current_user: Annotated[UserResponse, Depends(get_current_active_user)]
):
    user_data = await get_user_by_id(id)
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user_data


@user_router.get("/user", response_model=list[UserResponse])
async def get_users_router(
    current_user: Annotated[UserResponse, Depends(get_current_active_user)]
):
    return await get_all_users()


@user_router.put("/user/{id}", response_model=UserResponse)
async def update_user_router(
    id: str,
    user: UserCreate,
    current_user: Annotated[UserResponse, Depends(get_current_active_user)],
):
    user_data = user.model_dump(exclude_unset=True)
    if not await update_user(id, user_data):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return await get_user_by_id(id)


@user_router.delete("/user/{id}")
async def delete_user_router(
    id: str, current_user: Annotated[UserResponse, Depends(get_current_active_user)]
):
    if not await delete_user(id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return {"message": f"The user with id '{id}' is deleted successfully"}
