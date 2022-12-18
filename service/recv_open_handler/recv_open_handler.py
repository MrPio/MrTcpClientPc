import abc


class RecvOpenHandler(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def process(self, msg: bytes) -> None:
        pass

    @abc.abstractmethod
    def stop(self) -> None:
        pass