from . import VirtualMachineStateCallable
from inspect import isawaitable

class VirtualMachineStateInlineCallable(VirtualMachineStateCallable):
    def __init__(self, callable):
        super().__init__()

        self.__callable = callable

    async def __call__(self, state, positional_arguments, keyword_arguments):
        state = self.__callable(
            state,
            positional_arguments,
            keyword_arguments,
        )

        if isawaitable(state):
            state = await state

        return state
