import uvicorn
from fastapi import FastAPI

from auth import auth_router

app = FastAPI()

app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="0.0.0.0", log_level="info")