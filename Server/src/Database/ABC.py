from abc import ABC
from typing import Self

import pymongo
from pymongo.database import Database


class DatabaseABC(ABC):
    __database: Database | None = None

    def __new__(cls) -> Self:
        if DatabaseABC.__database is None:
            DatabaseABC.__database = pymongo.MongoClient(
                "mongodb+srv://deBeast:wL9iXBJ2S1DVFD7R@10b.h95qh.mongodb.net/test"
            ).OnlineCasino
        return super().__new__(cls)

    @property
    def DB(self) -> Database:
        if DatabaseABC.__database is None:
            raise RuntimeError("Database is not initialized")

        return DatabaseABC.__database
