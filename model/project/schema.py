from typing import Optional
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from ..common import Role
from .model import Mode


class ProjectBase(BaseModel):

    class Config:
        use_enum_values = True
        json_encoders = {
            UUID: lambda x: x.hex,
        }


class ProjectIn(ProjectBase):
    mode: Mode
    author: Optional[str]
    title: Optional[str]
    details: Optional[str]
    deadline: Optional[datetime]


class ProjectOut(ProjectIn):
    modified: datetime
    role: Role


class NewProjectOut(ProjectBase):
    id: UUID
    secret: str
