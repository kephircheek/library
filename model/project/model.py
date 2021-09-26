from enum import Enum
from uuid import uuid4
from datetime import datetime

from sqlalchemy import Table, Column, func
from sqlalchemy.dialects import postgresql as psql

from ..common import metadata, db
from ..tools import SecretToken


class Mode(str, Enum):
    INVITATION = 'INVITATION'


project = Table(
    "project",
    metadata,
    Column("id", psql.UUID(), primary_key=True, index=True),
    Column("mode", psql.ENUM(Mode), index=True),
    Column("secret", psql.BYTEA),
    Column("modified", psql.TIMESTAMP, server_default=func.now()),
    Column("title", psql.VARCHAR(30), default=None),
    Column("details", psql.VARCHAR(500), default=None),
    Column("deadline", psql.TIMESTAMP, default=None),
)


class Project:
    table = project

    @classmethod
    async def get(cls, id):
        return await db.fetch_one(project.select().where(project.c.id == id))

    @classmethod
    async def insert(cls, data):
        secret = SecretToken.gen(32)
        data.update({
            "id": uuid4(),
            "secret": secret.hash,
        })
        await db.execute(project.insert().values(**data))
        return {"id": data["id"], "secret": str(secret)}

    @classmethod
    async def update(cls, id, data):
        data['modified'] = datetime.utcnow()
        query = project.update().values(**data).where(project.c.id == id)
        return await db.execute(query)

    @classmethod
    async def delete(cls, id):
        return await db.execute(project.delete().where(project.c.id == id))
