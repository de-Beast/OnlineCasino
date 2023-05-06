__all__ = [
    "ThreadABC",
]

from abc import ABC, ABCMeta, abstractmethod
from typing import Self

import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore  # noqa: F401;
from PySide6.QtCore import (
    QMutex,
    QMutexLocker,
    QObject,
    QThread,
    QWaitCondition,
    Signal,
)

_ShibokenObjectType: type = type(QObject)


class _ShibokenObjectTypeFence(_ShibokenObjectType):
    ...


class _ResolverMeta(_ShibokenObjectTypeFence, ABCMeta, _ShibokenObjectType):
    ...


class QABC(ABC, metaclass=_ResolverMeta):
    """
    Абстрактный базовый класс для создания абстрактных классов,
    наследованных от классов `PySide6` (`QObject` и все, наследующиеся от него)

    ### Важно
    Данный класс должен стоять в начале при определении наследования

    ### Пример
    >>> class MyQtClass(QABC, QObject): ...
    """

    def __new__(cls, *args, **kwargs) -> Self:
        if hasattr(cls, "__abstractmethods__") and cls.__abstractmethods__.__len__() > 0:
            s = "s" if len(cls.__abstractmethods__) > 1 else ""
            raise TypeError(
                f"Can't instantiate abstract class {cls.__name__} "
                f'with abstract method{s} {", ".join(cls.__abstractmethods__)}'
            )

        return super().__new__(cls, *args, **kwargs)


class ThreadABC(QABC, QThread):
    """
    Абстрактный базовый класс для потоков.


    ### Абстрактные методы
    >>> def thread_workflow(self, *args, **kwargs) -> None: ...
    """

    # Таймаут, используемый в `wait_` методах
    wait_timeout: int = 10_000  # milliseconds

    error = Signal(str)

    @abstractmethod
    def thread_workflow(self, *args, **kwargs) -> None:
        raise NotImplementedError

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.finished.connect(self.delete_later)

        self._mutex = QMutex()
        self._cond = QWaitCondition()

        self._is_working: bool = False

    def __del__(self) -> None:
        self.stop_work()

    @property
    def is_working(self) -> bool:
        return self._is_working

    @property
    def mutex(self) -> QMutex:
        return self._mutex

    @property
    def cond(self) -> QWaitCondition:
        return self._cond

    def run(self) -> None:
        import sys

        if sys.argv.count("debug_threads") > 0:
            import debugpy  # type: ignore

            debugpy.debug_this_thread()

        self._is_working = True
        self.thread_workflow()
        self._is_working = False

    def stop_work(self) -> None:
        """
        Останавливает работу потока, если в методе `thread_workflow`
        был релизован цикл с использованием атрибута `is_working`.
        Также пробудит поток один раз, неважно, был ли он остановлен

        ### Пример 1

        В данном примере после `on_readyRead` атрибут `_is_working` переключится
        на значение `False`, и после того, как завершится метод `wait_for_readyRead`,
        цикл прервётся, поток закончит свою работу. Помните, что не стоит после такого цикла
        писать еще какой-либо код, не связанный с очисткой данных (сокет трогать не нужно)
        >>> def thread_workflow(self, socket):
        >>>     ...
        >>>     while self.is_working:
        >>>         ...
        >>>         socket.readyRead.connect(self.on_readyRead)
        >>>         self.wait_for_readyRead(socket)
        >>>
        >>> def on_readyRead(self):
        >>>     ...
        >>>     self.stop_work()

        ### Пример 2

        В данном примере наш поток блокируется, пускай есть метод, пробуждающий этот поток,
        после чего начинается новая итерация цикла. Из другого потока мы вызываем метод `stop_work`,
        из-за этого атрибут `_is_working` переключается в состояние `False`,
        а поток пробуждается и, в конечном счёте, заканчивает цикл и завершается
        >>> def thread_workflow(self, socket):
        >>>     ...
        >>>     while self.is_working:
        >>>         ...
        >>>         with QMutexLocker(self.mutex):
        >>>             self.cond.wait(self.mutex)
        >>>
        >>> ...
        >>> thread.stop_work()
        """

        with QMutexLocker(self.mutex):
            self._is_working = False
            self.cond.wake_one()
