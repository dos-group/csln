from abc import ABC, abstractmethod

class VirtualMachineStateCallable(ABC):
    @abstractmethod
    async def __call__(self, state, positional_arguments, keyword_arguments):
        pass
