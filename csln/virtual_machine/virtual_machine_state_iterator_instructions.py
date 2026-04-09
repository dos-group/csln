class VirtualMachineStateIteratorInstructions:
    def get_iter(self):
        return self.transition(
            stack=[
                *self.stack[:-1],
                iter(self.stack[-1]),
            ],
        )

    def for_iter(self):
        try:
            return self.transition(
                stack=[
                    *self.stack,
                    next(self.stack[-1]),
                ]
            )
        except StopIteration:
            return self.transition(
                stack=[
                    *self.stack[:-1]
                ],
                instruction_pointer=self.translate_instruction_delta(
                    self.current_instruction_jump_target,
                ),
            )
