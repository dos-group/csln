from . import VirtualMachineSymbolLoader

class VirtualMachineDefaultSymbolLoader(VirtualMachineSymbolLoader):
    def __init__(
            self,
            allowed_imports = None,
            disallowed_imports = None,
    ):
        super().__init__()

        self.allowed_imports = allowed_imports
        self.disallowed_imports = disallowed_imports

    async def load_import(self, state, import_name, level, from_list):
        if self.allowed_imports is not None and import_name not in self.allowed_imports:
            return None

        if self.disallowed_imports is not None and import_name in self.disallowed_imports:
            return None

        return __import__(import_name)

    async def load_name(self, state, name):
        return next(
            filter(
                lambda value: value is not None,
                map(
                    lambda dictionary: dictionary.get(name),
                    [
                        state.locals,
                        state.globals,
                    ]
                )
            ),
            None,
        )
