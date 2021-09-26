from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status

from .session import verify as verify_session
from .project.model import Project
from .item.model import Item
from .common import db

router = APIRouter()


@router.get("/{item_id}/project/{project_id}", dependencies=[Depends(verify_session)])
async def bind(item_id: UUID, project_id: UUID):
    if await Item.get(item_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such item")
    if await Project.get(project_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such project")
    project_ids = await Item.get_project_ids(item_id)
    if project_id in project_ids:
        raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED, detail="Already bound")
    project_ids.append(project_id)
    await Item.update(item_id, {"project_ids": project_ids})
    await Project.update(project_id, {})
    return Response(status_code=status.HTTP_201_CREATED)


@router.delete("/{item_id}/project/{project_id}", dependencies=[Depends(verify_session)])
async def unbind(item_id: UUID, project_id: UUID):
    if await Item.get(item_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such item")
    if await Project.get(project_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such project")
    project_ids = await Item.get_project_ids(item_id)
    if project_id not in project_ids:
        raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED, detail="Already unbound")
    project_ids.remove(project_id)
    await Item.update(item_id, {"project_ids": project_ids})
    await Project.update(project_id, {})
    return Response(status_code=status.HTTP_201_CREATED)
