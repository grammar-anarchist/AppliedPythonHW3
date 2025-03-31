import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from auth.router import auth_router
from links.router import links_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(links_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="0.0.0.0", log_level="info")
