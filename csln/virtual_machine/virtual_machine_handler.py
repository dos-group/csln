from abc import ABC, abstractmethod

class VirtualMachineHandler(ABC):
    @abstractmethod
    async def before_execute(self, state):
        pass

    @abstractmethod
    async def after_execute(self, state):
        pass

    @abstractmethod
    async def before_instruction_execute(self, state):
        pass

    @abstractmethod
    async def after_instruction_execute(self, state):
        pass

    @abstractmethod
    async def before_instruction_pointer_increment(self, state):
        pass

    @abstractmethod
    async def after_instruction_pointer_increment(self, state):
        pass

    @abstractmethod
    async def before_line_execute(self, state):
        pass

    @abstractmethod
    async def after_line_execute(self, state):
        pass
