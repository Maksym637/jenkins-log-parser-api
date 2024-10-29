import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from app.utils.constants import Dependencies as DP


load_dotenv()

client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
database = client.get_database(DP.DB_NAME)

user_collection = database.get_collection(DP.USER_COLLECTION)
jenkins_log_collection = database.get_collection(DP.JENKINS_LOG_COLLECTION)
jenkins_history_collection = database.get_collection(DP.JENKINS_HISTORY_COLLECTION)
