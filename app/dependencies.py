from motor.motor_asyncio import AsyncIOMotorClient


MONGO_DETAILS = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_DETAILS)

database = client.get_database("jenkins-log-parser-db")

user_collection = database.get_collection("users")
jenkins_log_collection = database.get_collection("jenkins_logs")
jenkins_history_collection = database.get_collection("jenkins_histories")
