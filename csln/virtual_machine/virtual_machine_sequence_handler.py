from . import VirtualMachineHandler
from inspect import isawaitable

class VirtualMachineSequenceHandler(VirtualMachineHandler):
    def __init__(self, handlers):
        self.__handlers = handlers

    async def before_execute(self, state):
        return await self.__handle("before_execute", state)

    async def after_execute(self, state):
        return await self.__handle("after_execute", state)

    async def after_instruction_execute(self, state):
        return await self.__handle("after_instruction_execute", state)

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
        for handler in self.__handlers:
            state = await getattr(self.__object, name)(state)

        return state
