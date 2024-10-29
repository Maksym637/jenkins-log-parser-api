import pytest
from httpx import AsyncClient
from fastapi import status
from tests.ancillary import get_headers, swapped_in_half


test_user_data = {
    "username": "kuser",
    "email": "kuser@gmail.com",
    "password": "Kuser123_",
    "is_active": True,
}


@pytest.mark.asyncio
async def test_create_jenkins_log_positive(async_client: AsyncClient):
    response_user = await async_client.post("/users", json=test_user_data)
    hashed_credentials = response_user.json()["hashed_credentials"]

    response_create = await async_client.post(
        "/jenkins-logs/me",
        json={"external_url": "http://192.168.0.112:8000/jenkins/101/log-file-txt"},
        headers=get_headers(hashed_credentials),
    )

    actual_chart_log_data = response_create.json()["chart_log_data"]
    expected_chart_log_data = {
        "passed": 66,
        "failed": 7,
        "errored": 11,
        "skipped": 1,
        "blocked": 0,
    }

    assert response_create.status_code == status.HTTP_200_OK
    assert actual_chart_log_data == expected_chart_log_data


@pytest.mark.asyncio
async def test_create_jenkins_log_negative(async_client: AsyncClient):
    response_user = await async_client.post("/users", json=test_user_data)
    hashed_credentials = response_user.json()["hashed_credentials"]

    response_create = await async_client.post(
        "/jenkins-logs/me",
        json={"external_url": "http://192.168.0.112:8000/jenkins/000/log-file-txt"},
        headers=get_headers(hashed_credentials),
    )

    assert response_create.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_get_jenkins_logs(async_client: AsyncClient):
    response_user = await async_client.post("/users", json=test_user_data)
    hashed_credentials = response_user.json()["hashed_credentials"]

    await async_client.post(
        "/jenkins-logs/me",
        json={"external_url": "http://192.168.0.112:8000/jenkins/101/log-file-txt"},
        headers=get_headers(hashed_credentials),
    )

    response_get = await async_client.get(
        "/jenkins-logs/me", headers=get_headers(hashed_credentials)
    )

    assert response_get.status_code == status.HTTP_200_OK
    assert len(response_get.json()) == 1
    assert isinstance(response_get.json(), list) == True


@pytest.mark.asyncio
async def test_get_jenkins_log_positive(async_client: AsyncClient):
    response_user = await async_client.post("/users", json=test_user_data)
    hashed_credentials = response_user.json()["hashed_credentials"]

    response_create = await async_client.post(
        "/jenkins-logs/me",
        json={"external_url": "http://192.168.0.112:8000/jenkins/101/log-file-txt"},
        headers=get_headers(hashed_credentials),
    )
    jenkins_log_id = response_create.json()["id"]

    response_get = await async_client.get(
        f"/jenkins-logs/me/{jenkins_log_id}", headers=get_headers(hashed_credentials)
    )

    assert response_get.status_code == status.HTTP_200_OK
    assert isinstance(response_get.json(), dict) == True


@pytest.mark.asyncio
async def test_get_jenkins_log_negative(async_client: AsyncClient):
    response_user = await async_client.post("/users", json=test_user_data)
    hashed_credentials = response_user.json()["hashed_credentials"]

    response_create = await async_client.post(
        "/jenkins-logs/me",
        json={"external_url": "http://192.168.0.112:8000/jenkins/101/log-file-txt"},
        headers=get_headers(hashed_credentials),
    )
    jenkins_log_id = response_create.json()["id"]

    response_get = await async_client.get(
        f"/jenkins-logs/me/{swapped_in_half(jenkins_log_id)}",
        headers=get_headers(hashed_credentials),
    )

    assert response_get.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_jenkins_log_positive(async_client: AsyncClient):
    pass


@pytest.mark.asyncio
async def test_delete_jenkins_log_negative(async_client: AsyncClient):
    pass
