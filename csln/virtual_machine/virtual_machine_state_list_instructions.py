class VirtualMachineStateListInstructions:
    def list_append(self):
        index = -self.current_instruction_argument  - 1

        return self.transition(
            stack=[
                *self.stack[:index],
                [
                    *self.stack[index],
                    self.stack[-1],
                ],
                *self.stack[index+1:-1],
            ],
        )

    def list_extend(self):
        index = -self.current_instruction_argument  - 1

        return self.transition(
            stack=[
                *self.stack[:index],
                [
                    *self.stack[index],
                    *list(self.stack[-1]),
                ],
                *self.stack[index + 1:-1],
            ],
        )
