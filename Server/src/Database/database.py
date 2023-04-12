from enum import Enum
from .ABC import DatabaseABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pymongo.collection import Collection


class CheckAccount(Enum):
    OK: int
    WRONG_LOGIN: int
    WRONG_PASSWORD: int


class AccountsDB(DatabaseABC):
    @property
    def accounts_collection(self) -> Collection:
        return self.DB.Accounts

    def check_account(self, account: dict) -> CheckAccount:
        data = self.accounts_collection.find_one(
            {"login": account["login"]}, {"_id": 0, "password": account["password"]}
        )
        if data is None:
            return CheckAccount.WRONG_LOGIN
        elif data["password"] != account["password"]:
            return CheckAccount.WRONG_PASSWORD
        
        return CheckAccount.OK
    
    def register_account(self, account: dict) -> bool:
        if not self.check_account(account):
            return False
        
        self.accounts_collection.insert_one(account)
        return True