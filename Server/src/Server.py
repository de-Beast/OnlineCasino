import sys

import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore  # noqa: F401
from PySide6.QtNetwork import QTcpServer

from abstract import ServerSocketThread
from games.roulette import Roulette
from Shared.slot_storage import SlotStorage


class Server(QTcpServer):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self._socket_threads: list[ServerSocketThread] = []

        if not self.listen(port=8888):
            print(self.error_string())
            sys.exit(1)
        else:
            print("Server started")

        Roulette().start()

    def incoming_connection(self, handle: int) -> None:
        socket_thread = ServerSocketThread(handle)
        self._socket_threads.append(socket_thread)
        socket_thread.finished.connect(SlotStorage.create_slot(self._socket_threads.remove, socket_thread))
        socket_thread.start()
