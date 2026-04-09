class VirtualMachineStateSetInstructions:
    def set_add(self):
        index = -self.current_instruction_argument  - 1

        return self.transition(
            stack=[
                *self.stack[:index],
                {
                    *self.stack[index],
                    self.stack[-1],
                },
                *self.stack[index + 1:-1],
            ],
        )

    def set_update(self):
        index = -self.current_instruction_argument  - 1

        return self.transition(
            stack=[
                *self.stack[:index],
                {
                    *self.stack[index],
                    *self.stack[-1],
                },
                *self.stack[index + 1:-1],
            ],
        )
