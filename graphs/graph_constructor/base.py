from abc import ABC, abstractmethod


class BaseGraphConstructMethod(ABC):

    @abstractmethod
    def construct(self, *args, **kwargs):
        pass
