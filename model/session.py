from typing import Optional, List, Union
from uuid import uuid4, UUID
import pickle

from pydantic import BaseModel
from fastapi import APIRouter, Depends, Response, Cookie, Header, HTTPException, status

# from .project.model import Project
from .common import redis, Role

router = APIRouter()


class Session:

    REDIS_KEY_PREFIX = "session:"

    @classmethod
    def load(cls, x_session_id: Optional[UUID] = Header(None)):
        return cls(x_session_id) if x_session_id else None

    def __init__(self, session_id: Union[UUID, str]):
        self._id = session_id if isinstance(session_id, UUID) else UUID(session_id)

    @property
    def hex(self):
        return self._id.hex

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self._id)})"

    async def set_project_role(self, id, role):
        await self.set(id.hex, Role.OWNER.name)

    async def get_project_role(self, id):
        return await self.get(id.hex, Role.MEMBER)

    async def get_released(self):
        return await self.get('released', [])

    async def append_release(self, data):
        released = await self.get_released()
        released.append(data)
        await self.set('released', released)

    async def remove_release(self, id):
        released = await self.get_released()
        await self.set('released', [r for r in released if r['id'] != id])

    @property
    def _key(self):
        return self.REDIS_KEY_PREFIX + self._id.hex

    @property
    async def data(self):
        value = await redis.get(self._key)
        return pickle.loads(value) if value else {}

    async def get(self, key, default=None):
        data = await self.data
        return data.get(key, default)

    async def set(self, key, value):
        data = await self.data
        data[key] = value
        return await redis.set(self._key, pickle.dumps(data))


def verify(session: Session = Depends(Session.load)):
    if session is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="permission denied"
        )



@router.get("/")
async def session(session: Session = Depends(Session.load)):
    return await session.data if session else {}


class Release(BaseModel):
    id: UUID
    secret: str

    class Config:
        json_encoders = {
            UUID: lambda x: x.hex,
        }

@router.get("/released", response_model=List[Release])
async def released(session: Session = Depends(Session.load)):
    return (await session.get_released()) if session else []
