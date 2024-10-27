import uvicorn
from fastapi import FastAPI
from dependencies import client
from utils.constants import Dependencies as DP
from routers.users import user_router
from routers.jenkins_logs import jenkins_log_router
from routers.jenkins_histories import jenkins_history_router


app = FastAPI()
app.include_router(user_router)
app.include_router(jenkins_log_router)
app.include_router(jenkins_history_router)


@app.on_event("shutdown")
async def shutdown_db_client():
    client.drop_database(DP.DB_NAME)
    client.close()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")
