import os
import enum
from pathlib import Path

from databases import Database
import aioredis
from sqlalchemy import MetaData
from dotenv import load_dotenv

db = Database(os.environ["DATABASE_URL"])
redis = aioredis.from_url(os.environ["REDIS_URL"])
metadata = MetaData()

class Role(enum.Enum):
    RANDOM = "RANDOM"
    MEMBER = 'MEMBER'
    OWNER = "OWNER"

