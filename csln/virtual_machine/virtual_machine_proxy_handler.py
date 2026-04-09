from . import VirtualMachineHandler
from inspect import isawaitable

class VirtualMachineProxyHandler(VirtualMachineHandler):
    def __init__(self, object, prefix=None):
        self.__object = object
        self.__prefix = prefix

    async def before_execute(self, state):
        return await self.__handle("before_execute", state)

    async def after_execute(self, state):
        return await self.__handle("after_execute", state)

    async def before_instruction_execute(self, state):
        return await self.__handle("before_instruction_execute", state)

    async def after_instruction_execute(self, state):
        return await self.__handle("after_instruction_execute", state)

    async def before_instruction_pointer_increment(self, state):
        return await self.__handle("before_instruction_pointer_increment", state)

    async def after_instruction_pointer_increment(self, state):
        return await self.__handle("after_instruction_pointer_increment", state)

    async def before_line_execute(self, state):
        return await self.__handle("before_line_execute", state)

    async def after_line_execute(self, state):
        return await self.__handle("after_line_execute", state)

    async def __handle(self, name, state):
        if self.__prefix is not None:
            name = self.__prefix + name

        if not hasattr(self.__object, name):
            return state

        result = getattr(self.__object, name)(state)

        if isawaitable(result):
            result = await result

        return result
