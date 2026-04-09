class VirtualMachineUnresolvedSymbolError(RuntimeError):
    def __init__(self, state, symbol_name):
        super().__init__("Unresolved symbol {}".format(symbol_name))

        self.__state = state
        self.__symbol_name = symbol_name

    @property
    def state(self):
        return self.__state

    @property
    def symbol_name(self):
        return self.__symbol_name
