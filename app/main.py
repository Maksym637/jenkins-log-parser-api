import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.dependencies import client, database
from app.utils.constants import Dependencies as DP
from app.routers.users import user_router
from app.routers.jenkins_logs import jenkins_log_router
from app.routers.jenkins_histories import jenkins_history_router


load_dotenv()

app = FastAPI(
    title="Jenkins log parser API",
    summary="This application handles unparsed Jenkins logs from external API",
)

app.include_router(user_router)
app.include_router(jenkins_log_router)
app.include_router(jenkins_history_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("API_URI"), os.getenv("APP_URI")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_db_client():
    if not database.name:
        raise IndentationError(
            f"Unable to establish connection to database '{DP.DB_NAME}'"
        )


@app.on_event("shutdown")
async def shutdown_db_client():
    client.drop_database(DP.DB_NAME)
    client.close()
