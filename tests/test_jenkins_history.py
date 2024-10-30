import pytest
from httpx import AsyncClient
from fastapi import status
from tests.ancillary import get_headers, swapped_in_half


test_user_data = {
    "username": "luser",
    "email": "luser@gmail.com",
    "password": "Luser123_",
    "is_active": True,
}


@pytest.mark.asyncio
async def test_get_jenkins_histories(async_client: AsyncClient):
    response_user = await async_client.post("/users", json=test_user_data)
    hashed_credentials = response_user.json()["hashed_credentials"]

    await async_client.post(
        "/jenkins-logs/me",
        json={"external_url": "http://192.168.0.112:8000/jenkins/105/log-file-txt"},
        headers=get_headers(hashed_credentials),
    )

    response_get = await async_client.get(
        "/jenkins-histories/me", headers=get_headers(hashed_credentials)
    )

    assert response_get.status_code == status.HTTP_200_OK
    assert len(response_get.json()) == 1
    assert isinstance(response_get.json(), list) == True


@pytest.mark.asyncio
async def test_get_jenkins_history_pan(async_client: AsyncClient):
    response_user = await async_client.post("/users", json=test_user_data)
    hashed_credentials = response_user.json()["hashed_credentials"]

    await async_client.post(
        "/jenkins-logs/me",
        json={"external_url": "http://192.168.0.112:8000/jenkins/105/log-file-txt"},
        headers=get_headers(hashed_credentials),
    )

    response_jenkins_histories = await async_client.get(
        "/jenkins-histories/me", headers=get_headers(hashed_credentials)
    )
    jenkins_history_id = response_jenkins_histories.json()[0]["id"]

    # -> Positive scenario
    response_get = await async_client.get(
        f"/jenkins-histories/me/{jenkins_history_id}",
        headers=get_headers(hashed_credentials),
    )

    assert response_get.status_code == status.HTTP_200_OK
    assert isinstance(response_get.json(), dict) == True

    # -> Negative scenario
    response_get = await async_client.get(
        f"/jenkins-histories/me/{swapped_in_half(jenkins_history_id)}",
        headers=get_headers(hashed_credentials),
    )

    assert response_get.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_jenkins_history_pan(async_client: AsyncClient):
    response_user = await async_client.post("/users", json=test_user_data)
    hashed_credentials = response_user.json()["hashed_credentials"]

    await async_client.post(
        "/jenkins-logs/me",
        json={"external_url": "http://192.168.0.112:8000/jenkins/105/log-file-txt"},
        headers=get_headers(hashed_credentials),
    )

    response_jenkins_histories = await async_client.get(
        "/jenkins-histories/me", headers=get_headers(hashed_credentials)
    )
    jenkins_history_id = response_jenkins_histories.json()[0]["id"]

    # -> Negative scenario
    response_delete = await async_client.delete(
        f"/jenkins-histories/me/{swapped_in_half(jenkins_history_id)}",
        headers=get_headers(hashed_credentials),
    )

    assert response_delete.status_code == status.HTTP_404_NOT_FOUND

    # -> Positive scenario
    response_delete = await async_client.delete(
        f"/jenkins-histories/me/{jenkins_history_id}",
        headers=get_headers(hashed_credentials),
    )
    actual_response_msg = response_delete.json()["message"]

    assert response_delete.status_code == status.HTTP_200_OK
    assert (
        actual_response_msg
        == f"The Jenkins history with id '{jenkins_history_id}' is deleted successfully"
    )
