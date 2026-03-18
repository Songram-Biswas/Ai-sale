from __future__ import annotations

from pymongo import MongoClient
from pymongo.collection import Collection

from app.config import settings


class MongoDB:
    def __init__(self, uri: str, db_name: str) -> None:
        self._uri = uri
        self._db_name = db_name
        self._client: MongoClient | None = None
        self._companies: Collection | None = None
        self._reports: Collection | None = None

    def connect(self) -> None:
        if self._client is None:
            self._client = MongoClient(self._uri)
            db = self._client[self._db_name]
            # collections are created on first insert in MongoDB; we keep handles here
            self._companies = db["companies"]
            self._reports = db["reports"]

    def close(self) -> None:
        if self._client is not None:
            self._client.close()
            self._client = None
        self._companies = None
        self._reports = None

    @property
    def db(self):
        if self._client is None:
            self.connect()
        assert self._client is not None
        return self._client[self._db_name]

    @property
    def companies(self) -> Collection:
        if self._companies is None:
            self.connect()
        assert self._companies is not None
        return self._companies

    @property
    def reports(self) -> Collection:
        if self._reports is None:
            self.connect()
        assert self._reports is not None
        return self._reports


mongodb = MongoDB(settings.mongo_uri, settings.mongo_db_name)

