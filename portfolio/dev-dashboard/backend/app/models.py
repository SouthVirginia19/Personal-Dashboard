from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text

from .database import Base


class CacheEntry(Base):
    __tablename__ = "cache"

    key = Column(String, primary_key=True)
    value = Column(Text, nullable=False)
    expires_at = Column(DateTime, nullable=False)


class Snapshot(Base):
    __tablename__ = "snapshots"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.utcnow, index=True)
    followers = Column(Integer, default=0)
    public_repos = Column(Integer, default=0)
    total_stars = Column(Integer, default=0)
    total_commits = Column(Integer, default=0)