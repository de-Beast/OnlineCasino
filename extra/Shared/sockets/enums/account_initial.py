from enum import IntEnum


class AccountInitialRequest(IntEnum):
    AUTH = 0
    REGISTER = 1


class AccountInitialResponse(IntEnum):
    AUTH_SUCCESS = 0
    AUTH_FAILURE_LOGIN = 1
    AUTH_FAILURE_PASSWORD = 2

    REGISTER_SUCCESS = 3
    REGISTER_FAILURE = 4
