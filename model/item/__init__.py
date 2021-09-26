from typing import Optional, List
from pathlib import Path
from datetime import datetime
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, status

from ..common import db
from ..session import Session, verify as verify_session
from .model import Item
from .schema import ItemId, ItemIn, ItemOut, Release

router = APIRouter()


@router.get("/", response_model=List[ItemOut])
async def select(project_id: UUID = None):
    if project_id:
        return await Item.select_project(project_id)

    items = await db.fetch_all(Item.table.select())
    return items


@router.post("/", response_model=ItemId)
async def append(data: ItemIn):
    data = await Item.insert(data.dict(exclude_unset=True))
    return data


@router.get("/{id}", response_model=ItemOut)
async def get(id: UUID):
    return await Item.get(id)


@router.put("/{id}", dependencies=[Depends(verify_session)])
async def update(id: UUID, data: ItemIn):
    return await Item.update(id, data.dict(exclude_unset=True))


@router.delete("/{id}", dependencies=[Depends(verify_session)])
async def delete(id: UUID):
    return await Item.delete(id)



@router.get("/{id}/release")
async def release(id: UUID, session: Session = Depends(Session.start)):
    await Item.update(id, {'relevance': False})
    secret = await Item.get_secret(id)
    await session.append_release({"id": id, "secret": str(secret)})
    return {"secret": str(secret)}


@router.delete("/{id}/release")
async def unrelease(id: UUID, secret: Optional[str], session: Session = Depends(Session.load)):
    if session:
        await session.remove_release(id)
    return await Item.update(id, {'relevance': True})


@router.get("/{id}/archive", dependencies=[Depends(verify_session)])
async def archive(id: UUID):
    await Item.update(id, {'archive': True})


@router.delete("/{id}/archive", dependencies=[Depends(verify_session)])
async def unarchive(id: UUID):
    return await Item.update(id, {'archive': False})
