from enum import Enum

from pymongo.collection import Collection

from .ABC import DatabaseABC


class DB_CheckAccountResponse(Enum):
    OK: int = 0
    WRONG_LOGIN: int = 1
    WRONG_PASSWORD: int = 2


class AccountsDB(DatabaseABC):
    @property
    def accounts_collection(self) -> Collection:
        return self.DB.Accounts

    def check_account(self, account: dict) -> DB_CheckAccountResponse:
        """
        Проверяет, совпадают ли логин и пароль данной учетной записи с теми, которые
        хранятся в базе данных

        ### Параметры

        - `account: dict`

        Параметр `account` представляет собой словарь, который содержит информацию о логине и пароле
        учетной записи пользователя вида `{"login": <login>, "password": <password>,
                                            "balance": <balance>, "nickname": <nickname>}`

        ### Возвращает

        Значение типа CheckAccountResponse, которое может быть одним из следующих вариантов:
        WRONG_LOGIN, WRONG_PASSWORD или OK.
        """

        data = self.accounts_collection.find_one({"login": account["login"]},
                                                 {"_id": 0, "password": 1})
        if data is None:
            return DB_CheckAccountResponse.WRONG_LOGIN
        elif data["password"] != account["password"]:
            return DB_CheckAccountResponse.WRONG_PASSWORD

        return DB_CheckAccountResponse.OK

    def register_account(self, account: dict) -> bool:
        """
        Принимает словарь, содержащий данные о логине и пароле пользователя,
        и пробует сохранить их в базе данных

        ### Параметры

        - `account: dict`

        Параметр `account` представляет собой словарь, который содержит информацию о логине и пароле
        учетной записи пользователя вида `{"login": <login>, "password": <password>}`

        ### Возвращает

        `True`, если данные пользователя успешно сохранены в базе данных.
        `False`, если пользователь с таким логином уже есть в базе данных
        """

        if self.check_account(account) is not DB_CheckAccountResponse.WRONG_LOGIN:
            return False
        extended_account = {**account, "balance": 0, "nickname": ""}
        self.accounts_collection.insert_one(extended_account)
        return True

    def get_account_info(self, login: str) -> dict | None:
        data: dict | None = self.accounts_collection.find_one({"login": login},
                                                 {"_id": 0, "balance": 1, "nickname": 1})
        return data