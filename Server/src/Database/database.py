from enum import Enum

from pymongo.collection import Collection

from .ABC import DatabaseABC


class CheckAccountResponse(Enum):
    OK: int = 0
    WRONG_LOGIN: int = 1
    WRONG_PASSWORD: int = 2


class AccountsDB(DatabaseABC):
    @property
    def accounts_collection(self) -> Collection:
        return self.DB.Accounts

    def check_account(self, account: dict) -> CheckAccountResponse:
        """
        Проверяет, совпадают ли логин и пароль данной учетной записи с теми, которые
        хранятся в базе данных

        ### Параметры

        - `account: dict`

        Параметр `account` представляет собой словарь, который содержит информацию о логине и пароле
        учетной записи пользователя вида `{"login": <login>, "password": <password>}`

        ### Возвращает

        Значение типа CheckAccountResponse, которое может быть одним из следующих вариантов:
        WRONG_LOGIN, WRONG_PASSWORD или OK.
        """

        data = self.accounts_collection.find_one({"login": account["login"]}, {"_id": 0, "password": 1})
        if data is None:
            return CheckAccountResponse.WRONG_LOGIN
        elif data["password"] != account["password"]:
            return CheckAccountResponse.WRONG_PASSWORD

        return CheckAccountResponse.OK

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

        if self.check_account(account) is not CheckAccountResponse.WRONG_LOGIN:
            return False

        self.accounts_collection.insert_one(account)
        return True
