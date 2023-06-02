from typing import NotRequired, TypedDict

from bson import ObjectId


class AccountInfo(TypedDict):
    _id: NotRequired[ObjectId]
    nickname: str
    balance: int
