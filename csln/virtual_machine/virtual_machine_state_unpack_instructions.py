class VirtualMachineStateUnpackInstructions:
    UNPACK_EX_BEFORE_BITMASK = 0xFF
    UNPACK_EX_AFTER_SHIFT = 8

    def unpack_sequence(self):
        return self.transition(
            stack=[
                *self.stack[:-1],
                *reversed(list(self.stack[-1]))
            ]
        )

    def unpack_ex(self):
        before = self.current_instruction_argument & VirtualMachineStateUnpackInstructions.UNPACK_EX_BEFORE_BITMASK
        after = self.current_instruction_argument >> VirtualMachineStateUnpackInstructions.UNPACK_EX_AFTER_SHIFT
        iterable = list(self.stack[-1])

        return self.transition(
            stack=[
                *self.stack[:-1],
                *reversed(iterable[len(iterable) - after:]),
                iterable[before:len(iterable) - after],
                *reversed(iterable[:before]),
            ]
        )
