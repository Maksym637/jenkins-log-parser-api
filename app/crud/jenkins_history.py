from bson import ObjectId
from dependencies import jenkins_history_collection
from schemas.jenkins_history import get_jenkins_history_in_db


async def get_jenkins_history_by_id(user_id: str, jenkins_history_id: str) -> dict:
    jenkins_history = await jenkins_history_collection.find_one(
        {"_id": ObjectId(jenkins_history_id), "user_id": user_id}
    )
    if jenkins_history:
        return get_jenkins_history_in_db(jenkins_history)
    return None


async def get_all_jenkins_histories(user_id: str) -> list[dict]:
    jenkins_histories = []
    async for jenkins_history in jenkins_history_collection.find({"user_id": user_id}):
        jenkins_histories.append(get_jenkins_history_in_db(jenkins_history))
    return jenkins_histories


async def delete_jenkins_history_by_id(user_id: str, jenkins_history_id: str) -> dict:
    jenkins_history = await jenkins_history_collection.find_one(
        {"_id": ObjectId(jenkins_history_id), "user_id": user_id}
    )
    if jenkins_history:
        await jenkins_history_collection.delete_one(
            {"_id": ObjectId(jenkins_history_id), "user_id": user_id}
        )
        return True
    return False
