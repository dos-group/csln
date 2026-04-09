from . import VirtualMachineHandler

class VirtualMachineNoOperationHandler(VirtualMachineHandler):
    async def before_execute(self, state):
        return state

    async def after_execute(self, state):
        return state

    async def before_instruction_execute(self, state):
        return state

    async def after_instruction_execute(self, state):
        return state

    async def before_instruction_pointer_increment(self, state):
        return state

    async def after_instruction_pointer_increment(self, state):
        return state

    async def before_line_execute(self, state):
        return state

    async def after_line_execute(self, state):
        return state
