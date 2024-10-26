import uvicorn
from fastapi import FastAPI
from dependencies import client
from routers.users import user_router


app = FastAPI()

app.include_router(user_router)


@app.on_event("shutdown")
async def shutdown_db_client():
    client.drop_database("jenkins-log-parser-db")
    client.close()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
