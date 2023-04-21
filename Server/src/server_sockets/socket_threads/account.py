import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore  # noqa: F401
from PySide6.QtNetwork import QTcpSocket

from .ABC import ServerSocketThreadABC


class AccountSocketThread(ServerSocketThreadABC):
    def thread_workflow(self, socket: QTcpSocket) -> None:
        pass
