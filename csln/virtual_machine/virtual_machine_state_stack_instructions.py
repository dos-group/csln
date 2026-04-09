class VirtualMachineStateStackInstructions:
    def push_null(self):
        return self.transition(
            stack=[
                *self.stack,
                None,
            ],
        )

    def pop_top(self):
        return self.transition(
            stack=[
                *self.stack[:-1],
            ]
        )
