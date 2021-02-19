from abc import abstractmethod, ABC


class InstrumentBase(ABC):
    @abstractmethod
    def underlying_entity(self):
        pass
