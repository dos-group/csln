from . import VirtualMachineHandler
from inspect import isawaitable

class VirtualMachineInlineHandler(VirtualMachineHandler):
    def __init__(self, **keyword_arguments):
        self.__handlers = keyword_arguments

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
        if name not in self.__handlers:
            return state

        result = self.__handlers[name](state)

        if isawaitable(result):
            result = await result

        return result
