from . import (
    VirtualMachineStateCallable,
    VirtualMachineStateExternalCallable,
    VirtualMachineStateInternalCallable,
)

class VirtualMachineStateFunctionInstructions:
    MAKE_FUNCTION_DEFAULTS_FLAG = 0x1
    MAKE_FUNCTION_KEYWORD_DEFAULTS_FLAG = 0x2
    MAKE_FUNCTION_ANNOTATIONS_FLAG = 0x4
    MAKE_FUNCTION_CLOSURE_FLAG = 0x8

    def make_function(self):
        index = 1 + sum(
            1
            for flag in (
                    VirtualMachineStateFunctionInstructions.MAKE_FUNCTION_DEFAULTS_FLAG,
                    VirtualMachineStateFunctionInstructions.MAKE_FUNCTION_KEYWORD_DEFAULTS_FLAG,
                    VirtualMachineStateFunctionInstructions.MAKE_FUNCTION_ANNOTATIONS_FLAG,
                    VirtualMachineStateFunctionInstructions.MAKE_FUNCTION_CLOSURE_FLAG,
            )
            if self.current_instruction_argument & flag
        )

        return self.transition(
            stack=[
                *self.stack[:-index],
                VirtualMachineStateInternalCallable(self.stack[-1]),
            ]
        )

    def kw_names(self):
        return self.transition(
            pending_keyword_names=self.current_instruction_argument_value,
        )

    async def call(self):
        callable = self.stack[-1-self.current_instruction_argument]

        if not isinstance(callable, VirtualMachineStateCallable):
            callable = VirtualMachineStateExternalCallable(callable)

        arguments = self.stack[-1:-self.current_instruction_argument-1:-1]

        return await callable(
            self.transition(
                stack=self.stack[:-2 - self.current_instruction_argument],
                pending_keyword_names=[],
            ),
            reversed(arguments[len(self.pending_keyword_names):]),
            dict(
                zip(
                    self.pending_keyword_names,
                    arguments[:len(self.pending_keyword_names)],
                )
            ),
        )

    def return_const(self):
        return self.transition(
            return_value_instance=self.current_instruction_argument_value,
        )

    def return_value(self):
        return self.transition(
            stack=self.stack[:-1],
            return_value_instance=self.stack[-1],
        )
