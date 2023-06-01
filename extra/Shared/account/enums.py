__all__ = [
    "AccountInitialRequest",
    "AccountInitialResponse",
]

from enum import auto

from ..abstract import EnumBase


class AccountInitialRequest(EnumBase):
    AUTH = auto()
    REGISTER = auto()


class AccountInitialResponse(EnumBase):
    AUTH_SUCCESS = auto()
    AUTH_FAILURE_LOGIN = auto()
    AUTH_FAILURE_PASSWORD = auto()

    REGISTER_SUCCESS = auto()
    REGISTER_FAILURE = auto()
