class VirtualMachineStateCommonInstructions:
    def next_instruction(self):
        return self.transition(
            instruction_pointer=self.instruction_pointer + 1,
        )

    def no_operation(self):
        return self

    def nop(self):
        return self.transition()

    def resume(self):
        return self.transition()

    def setup_annotations(self):
        return self.transition(
            locals={
                **self.locals,
                "__annotations__": {},
            }
        )

    def swap(self):
        return self.transition(
            stack=[
                *self.stack[:-2],
                self.stack[-2],
                self.stack[-1],
            ],
        )

    def binary_slice(self):
        return self.transition(
            stack=[
                *self.stack[:-3],
                self.stack[-3][self.stack[-2]:self.stack[-1]],
            ],
        )
