from abc import ABC
from typing import TYPE_CHECKING, Self

import pymongo

if TYPE_CHECKING:
    from pymongo.database import Database


class DatabaseABC(ABC):
    __database: Database

    def __new__(cls) -> Self:
        if cls.__database is None:
            cls.__database = pymongo.MongoClient(
                "mongodb+srv://deBeast:wL9iXBJ2S1DVFD7R@10b.h95qh.mongodb.net/test"
            ).OnlineCasino
        return super().__new__(cls)

    @property
    def DB(self) -> Database:
        return self.__database  # type: ignore
