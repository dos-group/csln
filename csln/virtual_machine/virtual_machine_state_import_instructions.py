from . import VirtualMachineUnresolvedSymbolError

class VirtualMachineStateImportInstructions:
    async def import_name(self):
        module = await self.symbol_loader.load_import(
            self,
            self.current_instruction_argument_value,
            self.stack[:-1],
            self.stack[:-2],
        )

        if module is None:
            raise VirtualMachineUnresolvedSymbolError(
                self,
                self.current_instruction_argument_value,
            )

        return self.transition(
            stack=[
                self.stack[:-2],
            ],
        )

    async def import_from(self):
        return self.transition(
            stack=[
                *self.stack,
                getattr(self.stack[-1], self.current_instruction_argument_value),
            ],
        )
