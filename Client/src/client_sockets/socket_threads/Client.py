from functools import partial
from types import MethodType
from typing import Callable, Self, TypeAlias

from Shared.slot_storage import SlotCallableWithoutSender, SlotStorage

from .ABC import ClientSocketThreadABC

ClientSocketThread: TypeAlias = ClientSocketThreadABC


class Client:
    __instance: Self | None = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    def __init__(self) -> None:
        self._socket_threads: list[ClientSocketThread] = []
        self._token: str | None = None

    @staticmethod
    def register_socket_thread_class(cls: type) -> type:
        if not issubclass(cls, ClientSocketThread):
            return cls

        for method in cls.__dict__.values():
            if not getattr(method, "_for_client", False):
                continue

            def inner_func(
                method, self: Client, *args, responseReceived_slot: SlotCallableWithoutSender | None, **kwargs
            ):
                socket_thread = cls()
                self._socket_threads.append(socket_thread)
                socket_thread.finished.connect(SlotStorage.create_slot(self._socket_threads.remove, socket_thread))
                if responseReceived_slot is not None:
                    socket_thread.responseRecieved.connect(responseReceived_slot)
                method(socket_thread, *args, **kwargs)

            setattr(Client, method.__name__, MethodType(partial(inner_func, method), Client()))

        return cls

    @staticmethod
    def mark_socket_thread_method(func: Callable) -> Callable:
        setattr(func, "_for_client", True)
        return func

    def auth(self, login: str, password: str, *, responseReceived_slot: SlotCallableWithoutSender | None) -> None:
        """Смотрите документацию `AccountInitialSocketThread.auth`"""

    def register(self, login: str, password: str, *, responseReceived_slot: SlotCallableWithoutSender | None) -> None:
        """Смотрите документацию `AccountInitialSocketThread.register`"""

    def get_account_info(self, login: str, *, responseReceived_slot: SlotCallableWithoutSender | None) -> None:
        """Смотрите документацию `AccountInfoSocketThread.get_account_info`"""
