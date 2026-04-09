class VirtualMachineStateStoreInstructions:
    def store_fast(self):
        return self.transition(
            locals={
                **self.locals,
               self.current_instruction_argument_value: self.stack[-1]
            },
            stack=[
                *self.stack[:-1],
            ]
        )

    def store_name(self):
        return self.transition(
           locals={
               **self.locals,
               self.current_instruction_argument_value: self.stack[-1]
           },
           stack=[
               *self.stack[:-1],
           ]
        )

    def store_global(self):
        return self.transition(
            globals={
                **self.globals,
                self.current_instruction_argument_value: self.stack[-1],
            },
            stack=self.stack[:-1],
        )

    def store_attr(self):
        setattr(
            self.stack[-2],
            self.current_instruction_argument_value,
            self.stack[-1],
        )

        return self.transition(
            stack=self.stack[:-2],
        )

    def store_subscr(self):
        self.stack[-2][self.stack[-1]] = self.stack[-3]

        return self.transition(
            stack=self.stack[:-3],
        )

    def store_deref(self):
        return self.transition(
            cells={
                **self.cells,
                self.current_instruction_argument_value: self.stack[-1],
            },
            stack=self.stack[:-1],
        )
