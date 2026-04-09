from . import (
    VirtualMachineStateBuildInstructions,
    VirtualMachineStateCommonInstructions,
    VirtualMachineStateDictInstructions,
    VirtualMachineStateFormatInstructions,
    VirtualMachineStateFunctionInstructions,
    VirtualMachineStateImportInstructions,
    VirtualMachineStateIteratorInstructions,
    VirtualMachineStateJumpInstructions,
    VirtualMachineStateListInstructions,
    VirtualMachineStateLoadInstructions,
    VirtualMachineStateMapInstructions,
    VirtualMachineStateOperatorInstructions,
    VirtualMachineStateSetInstructions,
    VirtualMachineStateStackInstructions,
    VirtualMachineStateStoreInstructions,
    VirtualMachineStateUnpackInstructions,
    VirtualMachineDefaultSymbolLoader,
)
from dis import get_instructions
from ast import walk, FunctionDef, Name, parse

class VirtualMachineState(
        VirtualMachineStateBuildInstructions,
        VirtualMachineStateCommonInstructions,
        VirtualMachineStateDictInstructions,
        VirtualMachineStateFormatInstructions,
        VirtualMachineStateFunctionInstructions,
        VirtualMachineStateImportInstructions,
        VirtualMachineStateIteratorInstructions,
        VirtualMachineStateJumpInstructions,
        VirtualMachineStateListInstructions,
        VirtualMachineStateLoadInstructions,
        VirtualMachineStateMapInstructions,
        VirtualMachineStateOperatorInstructions,
        VirtualMachineStateSetInstructions,
        VirtualMachineStateStackInstructions,
        VirtualMachineStateStoreInstructions,
        VirtualMachineStateUnpackInstructions,
        object,
):
    def __init__(
            self,
            virtual_machine,
            code,
            program,
            instructions,
            instruction_pointer = 0,
            globals= None,
            locals= None,
            stack= None,
            cells = None,
            pending_keyword_names = None,
            return_value_instance = None,
            root_state= None,
            previous_state= None,
            frames=None,
            context=None,
            symbol_loader=None,
    ):
        if globals is None:
            globals = {}

        if locals is None:
            locals = {}

        if stack is None:
            stack = []

        if cells is None:
            cells = {}

        if root_state is None:
            root_state = self

        if frames is None:
            frames = [self]
        else:
            frames = [*frames, self]

        if symbol_loader is None:
            symbol_loader = VirtualMachineDefaultSymbolLoader()

        self.virtual_machine = virtual_machine
        self.program = program
        self.code = code
        self.instructions = instructions
        self.instruction_pointer = instruction_pointer
        self.globals = globals
        self.locals = locals
        self.cells = cells
        self.stack = stack
        self.return_value_instance = return_value_instance
        self.pending_keyword_names = pending_keyword_names or []
        self.root_state = root_state
        self.previous_state = previous_state
        self.frames = frames
        self.context = context
        self.symbol_loader = symbol_loader

    @property
    def current_instruction(self):
        if self.instruction_pointer >= len(self.instructions):
            return None

        return self.instructions[self.instruction_pointer]

    @property
    def current_instruction_argument_value(self):
        return self.current_instruction.argval

    @property
    def current_instruction_operation_name(self):
        if self.current_instruction is None:
            return None

        return self.current_instruction.opname.lower()

    @property
    def current_instruction_argument(self):
        return self.instructions[self.instruction_pointer].arg

    @property
    def current_instruction_argument_count(self):
        return self.instructions[self.instruction_pointer].arg

    @property
    def current_instruction_argument_name_index(self):
        return self.instructions[self.instruction_pointer].arg

    @property
    def current_instruction_jump_target(self):
        return self.instructions[self.instruction_pointer].argval

    @property
    def is_root(self):
        return self == self.root_state

    @property
    def is_finished(self):
        return self.instruction_pointer >= len(self.instructions)

    def transition(self, **keyword_arguments):
        return VirtualMachineState(
            **{
                "virtual_machine": self.virtual_machine,
                "code": self.code,
                "program": self.program,
                "instructions": self.instructions,
                "instruction_pointer": self.instruction_pointer,
                "globals": self.globals,
                "locals": self.locals,
                "stack": self.stack,
                "root_state": self.root_state,
                "previous_state": self,
                "frames": self.frames[:-1],
                "context": self.context,
                "pending_keyword_names": self.pending_keyword_names,
                "symbol_loader": self.symbol_loader,
                **keyword_arguments,
            }
        )

    @property
    def source(self):
        return self.program.split("\n")

    @property
    def ast(self):
        return parse(self.program)

    def translate_instruction_delta(self, delta):
        return {
            instruction.offset: index for index, instruction in enumerate(self.instructions)
        }[delta]

    def reload(self, code):
        # TODO: Call Stack Support

        i = 0
        instructions = list(get_instructions(code))

        for instruction in instructions:
            if instruction.positions is not None and self.current_instruction is not None:
                if instruction.positions.lineno == self.current_instruction.positions.lineno:
                    break

            i = i + 1

        return self.transition(
            code=compile(code.encode("utf-8"), "<string>", "exec"),
            instructions=instructions,
            instruction_pointer=i,
            program=code,

        )

    def get_line_evaluation(self, line_number):
        non_callable_locals = set(
            filter(
                lambda key: not callable(self.locals[key]),
                self.locals.keys(),
            )
        )

        names = []

        for node in walk(self.ast):
            if not hasattr(node, 'lineno') or node.lineno != line_number:
                continue

            if isinstance(node, Name):
                names.append(node.id)

                continue

            if isinstance(node, FunctionDef):
                names.extend(map(lambda arg: arg.arg, node.args.args))
                names.extend(map(lambda arg: arg.arg, node.args.kwonlyargs))

                continue

        return dict(
            list(
                map(
                    lambda key: (key, self.locals[key]),
                    set(names) & non_callable_locals
                )
            )
        )

    @property
    def current_line_number(self):
        instruction = self.current_instruction
        if instruction is None:
            return None

        return instruction.positions.lineno

    @property
    def current_line_index(self):
        line_number = self.current_line_number
        if line_number is None:
            return None

        return line_number - 1
