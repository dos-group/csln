from . import  VirtualMachineStateCallable

class VirtualMachineStateInternalCallable(VirtualMachineStateCallable):
    def __init__(self, code):
        super().__init__()

        self.__code = code

    async def __call__(self, state, positional_arguments, keyword_arguments):
        callable_state = await state.virtual_machine.execute_code(
            self.__code,
            state.program,
            globals=state.globals,
            locals=dict(zip(self.__code.co_varnames, positional_arguments)),
            root_state=state.root_state,
            previous_state=state,
            frames=state.frames,
        )

        return state.transition(
            stack=[
                *state.stack,
                callable_state.return_value_instance,
            ],
        )
