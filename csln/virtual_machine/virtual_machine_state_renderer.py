class VirtualMachineStateRenderer:
    def render(self, state):
        def render_line(index, line):
            return "{} {}: {}{}".format(
                {
                    False:  "  ",
                    True: "->"
                }[state.current_line_index is not None and index == state.current_line_index],
                self.__render_line_number(index, len(state.source)),
                state.source[index],
                self.__render_line_attachments(state, index)
            )

        return "\n".join(
            map(
                lambda x: render_line(*x),
                enumerate(state.source),
            )
        )

    def __render_line_number(self, line_index, maximum_lines):
        return (len(str(maximum_lines)) - len(str(line_index + 1))) * " " + str(line_index + 1)

    def __render_line_attachments(self, state, line_index):
        evaluations = state.get_line_evaluation(line_index + 1)

        result = ", ".join(
            map(
                lambda key: "{} = {}".format(key, evaluations[key]),
                evaluations.keys(),
            )
        )

        return "{}{}".format(
            {
                True: "",
                False: " # ",
            }[len(result) == 0],
            result,
        )
