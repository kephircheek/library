from typing import Optional, Dict
from pathlib import Path
from datetime import datetime
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, status

from ..common import Role
from ..session import Session, verify as verify_session
from .model import Project
from .schema import ProjectIn, ProjectOut, NewProjectOut

router = APIRouter()


@router.post("/", response_model=NewProjectOut)
async def append(project: ProjectIn, session: Session = Depends(Session.start)):
    """Return ID of new wishlist."""
    data = await Project.insert(project.dict(exclude_unset=True))
    await session.set_project_role(data['id'], Role.OWNER)
    return data


@router.get("/{id}", response_model=ProjectOut)
async def get(id: UUID, session: Session = Depends(Session.load)):
    data = await Project.get(id)
    if data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found"
        )

    data = dict(data)
    if session:
        data['role'] = await session.get_project_role(id)
    else:
        data['role'] = Role.MEMBER
    return data


@router.put("/{project_id}", dependencies=[Depends(verify_session)])
async def update(project_id: UUID, project: ProjectIn):
    return await Project.update(project_id, project.dict(exclude_unset=True))


@router.delete("/{project_id}", dependencies=[Depends(verify_session)])
async def delete(project_id: UUID):
    # TODO: delete bindings
    return await Project.delete(project_id)
