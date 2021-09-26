from enum import Enum
from uuid import uuid4
from datetime import datetime

from sqlalchemy import Table, Column, func
from sqlalchemy.dialects import postgresql as psql

from ..common import metadata, db
from ..tools import SecretToken


class ItemMode(str, Enum):
    WISH = 'WISH'


item = Table(
    "item",
    metadata,
    Column("id", psql.UUID(), primary_key=True, index=True),
    Column("mode", psql.ENUM(ItemMode, name="item_mode", create_type=False), index=True),
    Column("archive", psql.BOOLEAN, server_default="false"),
    Column("secret", psql.BYTEA),
    Column("modified", psql.TIMESTAMP, server_default=func.now()),
    Column("title", psql.VARCHAR(32), nullable=True),
    Column("link", psql.VARCHAR(512), nullable=True),
    Column("cost", psql.INTEGER, nullable=True),
    Column("relevance", psql.BOOLEAN, server_default="true"),
    Column("project_ids", psql.ARRAY(psql.UUID), nullable=True),
)


class Item:
    table = item

    @classmethod
    async def get(cls, id):
        return await db.fetch_one(item.select().where(item.c.id == id))

    @classmethod
    async def get_project_ids(cls, id):
        query = item.select() \
                    .with_only_columns(item.c.project_ids) \
                    .where(item.c.id == id)
        data = await db.fetch_one(query)
        return data['project_ids'] or []

    @classmethod
    async def get_secret(cls, id) -> SecretToken:
        query = item.select() \
                .with_only_columns(item.c.secret) \
                .where(item.c.id == id)
        data = await db.fetch_one(query)
        return SecretToken(data['secret'])

    @classmethod
    async def select_project(cls, project_id):
        query = item.select().where(item.c.project_ids.contains([project_id]))
        return await db.fetch_all(query)

    @classmethod
    async def insert(cls, data):
        data.update({"id": uuid4(), "secret": bytes(SecretToken.gen(4))})
        await db.execute(item.insert().values(**data))
        return {"id": data["id"]}

    @classmethod
    async def update(cls, id, data):
        data['modified'] = datetime.utcnow()
        query = item.update().values(**data).where(item.c.id == id)
        return await db.execute(query)

    @classmethod
    async def delete(cls, id):
        return await db.execute(item.delete().where(item.c.id == id))
