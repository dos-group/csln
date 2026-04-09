from abc import ABC, abstractmethod

class VirtualMachineSymbolLoader(ABC):
    @abstractmethod
    async def load_import(self, state, import_name, level, from_list):
        pass

    @abstractmethod
    async def load_name(self, state, name):
        pass
