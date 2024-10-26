from bson import ObjectId
from dependencies import user_collection
from schemas.user import get_user_in_db


async def create_user(user_data: dict) -> dict:
    user = await user_collection.insert_one(user_data)
    created_user = await user_collection.find_one({"_id": ObjectId(user.inserted_id)})
    return get_user_in_db(created_user)


async def get_user_by_id(user_id: str) -> dict:
    user = await user_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        return get_user_in_db(user)
    return None


async def get_user_by_username(username: str) -> dict:
    user = await user_collection.find_one({"username": username})
    if user:
        return get_user_in_db(user)
    return None


async def get_all_users() -> list[dict]:
    users = []
    async for user in user_collection.find():
        users.append(get_user_in_db(user))
    return users


async def update_user(user_id: int, data: dict) -> bool:
    if not data:
        return False

    user = await user_collection.find_one({"_id": ObjectId(user_id)})

    if user:
        updated_user = await user_collection.update_one(
            {"_id": ObjectId(user_id)}, {"$set": data}
        )
        if updated_user:
            return True

    return False


async def delete_user(user_id: str) -> bool:
    user = await user_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        await user_collection.delete_one({"_id": ObjectId(user_id)})
        return True
    return False
