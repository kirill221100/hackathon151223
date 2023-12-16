from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from security.config import get_config
from routes.auth import auth_router
from routes.bed import bed_router
from routes.plant import plant_router
from routes.thread import thread_router
from routes.message import message_router
from db.db_setup import init_db
import uvicorn


@asynccontextmanager
async def on_startup(app: FastAPI):
    await init_db()
    yield

app = FastAPI(debug=get_config().DEBUG, lifespan=on_startup, title='SmartGarden API')
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(auth_router, prefix='/auth', tags=['auth'])
app.include_router(bed_router, prefix='/bed', tags=['bed'])
app.include_router(plant_router, prefix='/plant', tags=['plant'])
app.include_router(thread_router, prefix='/thread', tags=['thread'])
app.include_router(message_router, prefix='/message', tags=['message'])


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
