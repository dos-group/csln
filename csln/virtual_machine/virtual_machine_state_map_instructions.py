class VirtualMachineStateMapInstructions:
    def map_add(self):
        index = -self.current_instruction_argument - 1

        return self.transition(
            stack=[
                *self.stack[:index],
                {
                    **self.stack[index],
                    self.stack[-2]: self.stack[-1],
                },
                *self.stack[index + 1:-2],
            ],
        )
