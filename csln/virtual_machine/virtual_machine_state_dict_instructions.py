class VirtualMachineStateDictInstructions:
    def dict_update(self):
        index = -self.current_instruction_argument - 1

        return self.transition(
            stack=[
                *self.stack[:index],
                {
                    **self.stack[index],
                    **self.stack[-1],
                },
                *self.stack[index + 1:-1],
            ],
        )

    def dict_merge(self):
        index = -self.current_instruction_argument - 1

        return self.transition(
            stack=[
                *self.stack[:index],
                {
                    **self.stack[index],
                    **self.stack[-1],
                },
                *self.stack[index + 1:-1],
            ],
        )
