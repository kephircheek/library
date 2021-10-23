import os

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv; load_dotenv()

from .common import db
from . import project
from . import item
from . import bind
from . import session

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ["ALLOW_ORIGINS"].split(";"),
    allow_methods=["*"],
    allow_headers=[
        "x-session-id",
    ],
)

app.include_router(project.router, prefix='/project')
app.include_router(item.router, prefix='/item')
app.include_router(bind.router, prefix='/bind')
app.include_router(session.router, prefix='/session')


@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()


@app.get('/')
async def ping():
    return "pong"
