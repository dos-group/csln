from . import VirtualMachineStateCallable
from inspect import isawaitable

class VirtualMachineStateExternalCallable(VirtualMachineStateCallable):
    def __init__(self, callable):
        super().__init__()

        self.__callable = callable

    async def __call__(self, state, positional_arguments, keyword_arguments):
        result = self.__callable(
            *positional_arguments,
            **keyword_arguments,
        )

        if isawaitable(result):
            result = await result

        return state.transition(
            stack=[
                *state.stack,
                result,
            ]
        )
