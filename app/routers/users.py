from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
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
    create_basic_token,
    check_password_strength,
)


user_router = APIRouter()


@user_router.post(
    "/user",
    response_model=UserResponse,
    tags=["users"],
    description="Register user in the system",
)
async def create_user_router(user: UserCreate):
    user_in_system = await get_user_by_username(user.username)

    if user_in_system:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this username already exists in the system",
        )

    if not check_password_strength(user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Password must be at least 8 characters long, include one uppercase, "
                "lowercase letter, one digit and one special character"
            ),
        )

    user_data = user.model_dump(exclude={"password"})
    user_data["hashed_credentials"] = create_basic_token(user.username, user.password)

    return await create_user(user_data)


@user_router.post("/login", tags=["auth"], description="Login to the system")
async def login_router(user: UserLogin):
    user_in_system = await get_user_by_username(user.username)

    if not user_in_system or not is_credentials(
        user_in_system, user.username, user.password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    token = create_basic_token(user.username, user.password)

    return JSONResponse(
        content={"access_token": token, "token_type": "basic"},
        status_code=status.HTTP_200_OK,
    )


@user_router.post("/logout", tags=["auth"], description="Log out user from the system")
async def logout_router(
    current_user: Annotated[UserResponse, Depends(get_current_active_user)]
):
    return JSONResponse(
        content={"message": "Logged out successfully"}, status_code=status.HTTP_200_OK
    )


@user_router.get(
    "/user/{id}",
    response_model=UserResponse,
    tags=["users"],
    description="Get user by id",
)
async def get_user_router(
    id: str, current_user: Annotated[UserResponse, Depends(get_current_active_user)]
):
    user_in_system = await get_user_by_id(id)
    if not user_in_system:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user_in_system


@user_router.get(
    "/user",
    response_model=list[UserResponse],
    tags=["users"],
    description="Get all users",
)
async def get_users_router(
    current_user: Annotated[UserResponse, Depends(get_current_active_user)]
):
    return await get_all_users()


@user_router.put(
    "/user/{id}",
    response_model=UserResponse,
    tags=["users"],
    description="Update user by id",
)
async def update_user_router(
    id: str,
    user: UserCreate,
    current_user: Annotated[UserResponse, Depends(get_current_active_user)],
):
    user_in_system = await get_user_by_username(user.username)

    if user_in_system and user_in_system != current_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this username already exists in the system",
        )

    if not check_password_strength(user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Password must be at least 8 characters long, include one uppercase, "
                "lowercase letter, one digit and one special character"
            ),
        )

    user_data = user.model_dump(exclude={"password"}, exclude_unset=True)
    user_data["hashed_credentials"] = create_basic_token(user.username, user.password)

    if not await update_user(id, user_data):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return await get_user_by_id(id)


@user_router.delete("/user/{id}", tags=["users"], description="Delete user by id")
async def delete_user_router(
    id: str, current_user: Annotated[UserResponse, Depends(get_current_active_user)]
):
    if not await delete_user(id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return JSONResponse(
        content={"message": f"The user with id '{id}' is deleted successfully"},
        status_code=status.HTTP_200_OK,
    )
