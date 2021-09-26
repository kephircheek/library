from typing import Optional, Union, List
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel

from .model import ItemMode


class ItemBase(BaseModel):

    class Config:
        use_enum_values = True
        json_encoders = {
            UUID: lambda x: x.hex,
        }

class ItemId(ItemBase):
    id: UUID


class ItemIn(ItemBase):
    mode: ItemMode
    title: str
    link: Optional[str]
    cost: Optional[int]


class ItemOut(ItemId, ItemIn):
    archive: bool
    modified: datetime
    relevance: Optional[bool]
    project_ids: Union[List[UUID], None]


class Release(ItemBase):
    id: UUID
    mode: ItemMode
    title: str
    link: Optional[str]
    cost: Optional[int]
