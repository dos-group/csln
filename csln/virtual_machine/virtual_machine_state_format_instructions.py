class VirtualMachineStateFormatInstructions:
    def format_simple(self):
        return self.transition(
            stack=[
                *self.stack[:-1],
                str(self.stack[-1]),
            ],
        )

    def format_value(self):
        flags = self.current_instruction_argument
        has_format_spec = flags & 0x04
        conversion = flags & 0x03

        if has_format_spec:
            format_spec = self.stack[-1]
            value = self.stack[-2]
            new_stack = self.stack[:-2]
        else:
            format_spec = ""
            value = self.stack[-1]
            new_stack = self.stack[:-1]

        if conversion == 1:
            value = repr(value)
        elif conversion == 2:
            value = str(value)
        elif conversion == 3:
            value = ascii(value)

        return self.transition(
            stack=[*new_stack, format(value, format_spec)]
        )
