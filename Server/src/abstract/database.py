from abc import ABC
from typing import Self

import pymongo
from pymongo.database import Database as DB


class Database(ABC):
    __database: DB | None = None

    def __new__(cls) -> Self:
        if Database.__database is None:
            Database.__database = pymongo.MongoClient(
                "mongodb+srv://deBeast:wL9iXBJ2S1DVFD7R@10b.h95qh.mongodb.net/test"
            ).OnlineCasino
        return super().__new__(cls)

    @property
    def DB(self) -> DB:
        if Database.__database is None:
            raise RuntimeError("database is not initialized")

        return Database.__database
