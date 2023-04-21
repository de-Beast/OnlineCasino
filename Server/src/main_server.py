import PySide6  # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore  # noqa: F401
from PySide6.QtWidgets import QApplication

from Server import Server

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    server = Server()
    sys.exit(app.exec())
