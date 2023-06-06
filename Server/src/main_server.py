import PySide6  # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore  # noqa: F401
from PySide6.QtWidgets import QApplication

from server import Server


def setup():
    import account  # noqa: F401
    import chat  # noqa: F401
    import games  # noqa: F401


if __name__ == "__main__":
    import sys

    setup()

    app = QApplication(sys.argv)
    server = Server()
    sys.exit(app.exec())
