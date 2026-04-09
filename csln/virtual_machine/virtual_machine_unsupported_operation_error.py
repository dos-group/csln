class VirtualMachineUnsupportedOperationError(NotImplementedError):
    def __init__(self, state, operation_name):
        super().__init__("Unsupported operation {}".format(operation_name))

        self.__state = state
        self.__operation_name = operation_name

    @property
    def state(self):
        return self.__state

    @property
    def operation_name(self):
        return self.__operation_name
