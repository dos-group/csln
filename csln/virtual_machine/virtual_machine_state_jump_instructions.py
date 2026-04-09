class VirtualMachineStateJumpInstructions:
    def pop_jump_if_false(self):
        return self.transition(
            stack=[
                *self.stack[:-1],
            ],
            instruction_pointer={
                True: self.instruction_pointer,
                False: self.translate_instruction_delta(
                    self.current_instruction_argument_value,
                ) - 1,
            }[self.stack[-1]],
        )

    def pop_jump_if_true(self):
        return self.transition(
            stack=[
                *self.stack[:-1],
            ],
            instruction_pointer={
                False: self.translate_instruction_delta(
                    self.current_instruction_argument_value,
                ) - 1,
                True: self.instruction_pointer,
            }[self.stack[-1]],
        )

    def pop_jump_forward_if_false(self):
        return self.pop_jump_if_false()

    def pop_jump_backward_if_false(self):
        return self.pop_jump_if_false()

    def pop_jump_forward_if_true(self):
        return self.pop_jump_if_true()

    def pop_jump_backward_if_true(self):
        return self.pop_jump_if_true()

    def jump_backward(self):
        return self.transition(
            instruction_pointer=self.translate_instruction_delta(
                self.current_instruction_argument_value,
            ) - 1,
        )

    def jump_forward(self):
        return self.transition(
            instruction_pointer=self.translate_instruction_delta(
                self.current_instruction_argument_value,
            ) - 1,
        )
