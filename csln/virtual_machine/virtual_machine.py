from . import VirtualMachineNoOperationHandler, VirtualMachineState, VirtualMachineUnsupportedOperationError
from dis import get_instructions
from functools import reduce
from inspect import isawaitable

class VirtualMachine:
    def __init__(self, handler=None):
        if handler is None:
            handler = VirtualMachineNoOperationHandler()

        self.__handler = handler

    @property
    def handler(self):
        return self.__handler

    async def execute_string(self, string, **kwargs):
        return await self.execute_code(
            compile(string.encode("utf-8"), "<string>", "exec"),
            string,
            **kwargs,
        )

    async def execute_code(self, code, program, **kwargs):
        return await self.execute_instructions(
            code,
            program,
            list(get_instructions(code)),
            **kwargs,
        )

    async def execute_instructions(
            self,
            code,
            program,
            instructions,
            **kwargs,
    ):
        return await self.execute_state(
            VirtualMachineState(
                self,
                code,
                program,
                instructions,
                **kwargs,
            )
        )

    async def execute_file(
            self,
            file_path,
            **keyword_arguments,
    ):
        with open(file_path, "r") as handle:
            return await self.execute_string(handle.read(), **keyword_arguments)

    async def execute_state(self, state):
        state = await self.__handle_event("before_execute", state)

        while not state.is_finished:
            operation_name = state.current_instruction_operation_name

            if not hasattr(state, operation_name):
                raise VirtualMachineUnsupportedOperationError(state, operation_name)

            for i, step in enumerate([
                lambda state: self.__handle_event("before_instruction_execute", state),
                lambda state: (getattr(state, operation_name))(),
                lambda state: self.__handle_event("after_instruction_execute", state),
                lambda state: self.__handle_event("before_instruction_pointer_increment", state),
                lambda state: state.next_instruction(),
                lambda state: self.__handle_event("after_instruction_pointer_increment", state),
            ]):
                result = step(state)

                if isawaitable(result):
                    result = await result

                state = result

            if not state.is_finished:
                if not hasattr(self, 'last_key'):
                    self.last_key = None

                positions = state.current_instruction.positions
                if not(positions and positions.lineno):
                    continue

                key = positions.lineno

                if key != self.last_key:
                    state = await self.handler.before_line_execute(state)

                    self.last_key = key

            if state.is_finished:
                state = await self.__handle_event("after_execute", state)

        return state

    def __handle_event(self, event_name, state):
        return getattr(self.handler, event_name)(state)
