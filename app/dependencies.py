from motor.motor_asyncio import AsyncIOMotorClient
from utils.constants import Dependencies as DP


MONGO_DETAILS = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_DETAILS)

database = client.get_database(DP.DB_NAME)

user_collection = database.get_collection(DP.USER_COLLECTION)
jenkins_log_collection = database.get_collection(DP.JENKINS_LOG_COLLECTION)
jenkins_history_collection = database.get_collection(DP.JENKINS_HISTORY_COLLECTION)
