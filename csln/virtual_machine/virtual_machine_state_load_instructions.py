from . import VirtualMachineUnresolvedSymbolError

class VirtualMachineStateLoadInstructions:
    LOAD_GLOBAL_PUSH_NULL_FLAG = 0x1

    LOAD_ATTR_PUSH_NULL_FLAG = 0x1

    def load_attr(self):
        return self.transition(
            stack=[
                *self.stack[:-1],
                *{
                    True: [None],
                    False: [],
                }[self.current_instruction_argument & VirtualMachineStateLoadInstructions.LOAD_ATTR_PUSH_NULL_FLAG],
                getattr(self.stack[-1], self.current_instruction_argument_value),
            ],
        )

    def load_const(self):
        return self.transition(
            stack=[
                *self.stack,
                self.current_instruction_argument_value,
            ],
        )

    def load_fast(self):
        return self.transition(
            stack=[
                *self.stack,
                self.locals[self.current_instruction_argument_value]
            ],
        )

    async def load_name(self):
        item = await self.symbol_loader.load_name(
            self,
            self.current_instruction_argument_value,
        )

        if item is None:
            raise VirtualMachineUnresolvedSymbolError(
                self,
                self.current_instruction_argument_value,
            )

        return self.transition(
            stack=[
                *self.stack,
                item,
            ],
        )

    def load_global(self):
        return self.transition(
            stack=[
                *self.stack,
                *{
                    True: [None],
                    False: [],
                }[self.current_instruction_argument & VirtualMachineStateLoadInstructions.LOAD_GLOBAL_PUSH_NULL_FLAG],
                self.globals[self.current_instruction_argument_value],
            ],
        )

    def load_method(self):
        method = getattr(
            self.stack[-1],
            self.current_instruction_argument_value,
        ),

        def proxy(*arguments, **keyword_arguments):
            return method(
                *arguments,
                **keyword_arguments,
            )

        return self.transition(
            stack=[
                *self.stack[:-1],
                proxy,
                self.stack[-1],
            ],
        )

    def load_deref(self):
        return self.transition(
            stack=[
                *self.stack,
                self.cells[self.current_instruction_argument_value],
            ],
        )

    def load_closure(self):
        return self.transition(
            stack=[
                *self.stack,
                self.cells[self.current_instruction_argument_value],
            ],
        )

    def load_build_class(self):
        return self.transition(
            stack=[
                *self.stack,
                __build_class__,
            ],
        )

    def load_assertion_error(self):
        return self.transition(
            stack=[
                *self.stack,
                AssertionError,
            ],
        )
