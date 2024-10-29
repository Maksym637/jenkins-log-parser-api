import pytest
from httpx import AsyncClient
from fastapi import status


test_user_data = {
    "username": "tuser",
    "email": "tuser@gmail.com",
    "password": "Tuser123_",
    "is_active": True,
}

get_headers = lambda hashed_credentials: {
    "Authorization": f"Basic {hashed_credentials}"
}


@pytest.mark.asyncio
async def test_login_positive(async_client: AsyncClient):
    response_create = await async_client.post("/users", json=test_user_data)
    assert response_create.status_code == status.HTTP_200_OK

    response_login = await async_client.post(
        "/login",
        json={
            "username": test_user_data["username"],
            "password": test_user_data["password"],
        },
    )
    assert response_login.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_login_negative(async_client: AsyncClient):
    response = await async_client.post(
        "/login", json={"username": "invalid_user", "password": "wrong_password"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_logout_positive(async_client: AsyncClient):
    response_create = await async_client.post("/users", json=test_user_data)
    hashed_credentials = response_create.json()["hashed_credentials"]
    assert response_create.status_code == status.HTTP_200_OK

    response_logout = await async_client.post(
        "/logout", headers=get_headers(hashed_credentials)
    )
    assert response_logout.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_logout_negative(async_client: AsyncClient):
    response = await async_client.post("/logout")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_create_user_positive(async_client: AsyncClient):
    response_create = await async_client.post("/users", json=test_user_data)
    actual_data = response_create.json()

    actual_username, actual_email = actual_data["username"], actual_data["email"]
    expected_username, expected_email = (
        test_user_data["username"],
        test_user_data["email"],
    )

    assert response_create.status_code == status.HTTP_200_OK
    assert (actual_username, actual_email) == (expected_username, expected_email)


@pytest.mark.asyncio
async def test_create_user_negative(async_client: AsyncClient):
    # -> Scenario 1 (incorrect email)
    response_create = await async_client.post(
        "/users",
        json={
            "username": "tuser",
            "email": "...@gmail.com",
            "password": "Tuser123_",
            "is_active": True,
        },
    )
    assert response_create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # -> Scenario 2 (incorrect password)
    response_create = await async_client.post(
        "/users",
        json={
            "username": "tuser",
            "email": "tuser@gmail.com",
            "password": "1111",
            "is_active": True,
        },
    )
    assert response_create.status_code == status.HTTP_400_BAD_REQUEST

    # -> Scenario 3 (username duplication)
    await async_client.post("/users", json=test_user_data)
    response_create = await async_client.post("/users", json=test_user_data)
    actual_response_msg = response_create.json()["detail"]

    assert response_create.status_code == status.HTTP_400_BAD_REQUEST
    assert (
        actual_response_msg
        == "The user with this username already exists in the system"
    )


@pytest.mark.asyncio
async def test_get_users(async_client: AsyncClient):
    response_create = await async_client.post("/users", json=test_user_data)
    hashed_credentials = response_create.json()["hashed_credentials"]

    response_get = await async_client.get(
        "/users", headers=get_headers(hashed_credentials)
    )

    assert response_get.status_code == status.HTTP_200_OK
    assert len(response_get.json()) == 1
    assert isinstance(response_get.json(), list) == True


@pytest.mark.asyncio
async def test_get_user_positive(async_client: AsyncClient):
    response_create = await async_client.post("/users", json=test_user_data)
    user_id = response_create.json()["id"]
    hashed_credentials = response_create.json()["hashed_credentials"]

    response_get = await async_client.get(
        f"/users/{user_id}", headers=get_headers(hashed_credentials)
    )
    actual_username = response_get.json()["username"]
    expected_username = test_user_data["username"]

    assert response_get.status_code == status.HTTP_200_OK
    assert actual_username == expected_username


@pytest.mark.asyncio
async def test_get_user_negative(async_client: AsyncClient):
    response_create = await async_client.post("/users", json=test_user_data)

    user_id = response_create.json()["id"]
    hashed_credentials = response_create.json()["hashed_credentials"]

    user_id_first = user_id[0 : len(user_id) // 2]
    user_id_second = user_id[len(user_id) // 2 : len(user_id)]

    response_get = await async_client.get(
        f"/users/{user_id_second}{user_id_first}",
        headers=get_headers(hashed_credentials),
    )

    assert response_get.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_update_user_positive(async_client: AsyncClient):
    response_create = await async_client.post("/users", json=test_user_data)
    hashed_credentials = response_create.json()["hashed_credentials"]

    response_update = await async_client.put(
        "/users/me",
        json={
            "username": "tuser",
            "email": "tuser123@gmail.com",
            "password": "Tuser123_",
            "is_active": True,
        },
        headers=get_headers(hashed_credentials),
    )

    actual_email = response_update.json()["email"]
    expected_email = "tuser123@gmail.com"

    assert response_update.status_code == status.HTTP_200_OK
    assert actual_email == expected_email


@pytest.mark.asyncio
async def test_update_user_negative(async_client: AsyncClient):
    response_create = await async_client.post("/users", json=test_user_data)
    hashed_credentials = response_create.json()["hashed_credentials"]

    # -> Scenario 1 (incorrect email)
    response_update = await async_client.put(
        "/users/me",
        json={
            "username": "tuser",
            "email": "@gmail.com",
            "password": "Tuser123_",
            "is_active": True,
        },
        headers=get_headers(hashed_credentials),
    )
    assert response_update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # -> Scenario 2 (incorrect password)
    response_update = await async_client.put(
        "/users/me",
        json={
            "username": "tuser",
            "email": "tuser@gmail.com",
            "password": "12345678",
            "is_active": True,
        },
        headers=get_headers(hashed_credentials),
    )
    assert response_update.status_code == status.HTTP_400_BAD_REQUEST

    # -> Scenario 3 (username duplication)
    await async_client.post(
        "/users",
        json={
            "username": "ouser",
            "email": "ouser@gmail.com",
            "password": "Ouser123_",
            "is_active": True,
        },
    )
    response_update = await async_client.put(
        "/users/me",
        json={
            "username": "ouser",
            "email": "tuser@gmail.com",
            "password": "Tuser123_",
            "is_active": True,
        },
        headers=get_headers(hashed_credentials),
    )
    actual_response_msg = response_update.json()["detail"]

    assert response_update.status_code == status.HTTP_400_BAD_REQUEST
    assert (
        actual_response_msg
        == "The user with this username already exists in the system"
    )


@pytest.mark.asyncio
async def test_delete_user_positive(async_client: AsyncClient):
    response_create = await async_client.post("/users", json=test_user_data)
    hashed_credentials = response_create.json()["hashed_credentials"]

    response_delete = await async_client.delete(
        "/users/me", headers=get_headers(hashed_credentials)
    )
    actual_response_msg = response_delete.json()["message"]

    assert response_delete.status_code == status.HTTP_200_OK
    assert actual_response_msg == "You are deleted successfully"


@pytest.mark.asyncio
async def test_delete_user_negative(async_client: AsyncClient):
    await async_client.post("/users", json=test_user_data)
    response_delete = await async_client.delete("/users/me")
    assert response_delete.status_code == status.HTTP_401_UNAUTHORIZED
