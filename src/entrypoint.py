from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from src.cache.redis_connection import redis as redis_conn

from src.api.v1 import v1_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_conn.initialize()
    yield


app = FastAPI(
    title='Client data service',
    description="The service is designed to change the user's address by phone number",
    lifespan=lifespan,
    version='0.1.0',
    docs_url='/docs'
)

app.include_router(v1_router)

if __name__ == '__main__':
    uvicorn.run(
        'src.entrypoint:app',
        host='0.0.0.0',
        port=8000,
    )
