class VirtualMachineStateBuildInstructions:
    def build_const_key_map(self):
        return self.transition(
            stack=[
                *self.stack[:-(self.current_instruction_argument + 1)],
                dict(
                    zip(
                        self.stack[-1],
                        self.stack[-(self.current_instruction_argument + 1):-1],
                    ),
                ),
            ],
        )

    def build_map(self):
        return self.transition(
            stack=[
                *self.stack[:-(self.current_instruction_argument + 1)],
                dict(
                    zip(
                        self.stack[-1],
                        self.stack[-(self.current_instruction_argument + 1):-1],
                    ),
                ),
            ],
        )

    def build_tuple(self):
        if self.current_instruction_argument == 0:
            return self.transition(
                stack=[
                    *self.stack,
                    tuple(),
                ]
            )

        return self.transition(
            stack=[
                *self.stack[:-self.current_instruction_argument],
                tuple(self.stack[-self.current_instruction_argument:]),
            ]
        )

    def build_set(self):
        if self.current_instruction_argument == 0:
            return self.transition(
                stack=[
                    *self.stack,
                    set(),
                ]
            )

        return self.transition(
            stack=[
                *self.stack[:-self.current_instruction_argument],
                set(self.stack[-self.current_instruction_argument:]),
            ]
        )

    def build_list(self):
        if self.current_instruction_argument == 0:
            return self.transition(
                stack=[
                    *self.stack,
                    [],
                ]
            )

        return self.transition(
            stack=[
                *self.stack[:-self.current_instruction_argument],
                list(self.stack[-self.current_instruction_argument:]),
            ]
        )

    def build_string(self):
        return self.transition(
            stack=[
                *self.stack[:-self.current_instruction_argument],
                "".join(self.stack[-self.current_instruction_argument:]),
            ],
        )

    def build_list_from_arg(self):
        return self.transition(
            stack=[
                *self.stack[:-1],
                list(self.stack[-1])
            ]
        )
