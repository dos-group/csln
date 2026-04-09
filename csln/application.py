from .virtual_machine import VirtualMachine, VirtualMachineStateInlineCallable, VirtualMachineInlineHandler, VirtualMachineStateRenderer, VirtualMachineDefaultSymbolLoader
from .agent import HallucinatedWorkflowAgent, AgentSynthesizerAgent
from os import environ
from asyncio import run

class HallucinatedSymbolLoader(VirtualMachineDefaultSymbolLoader):
    async def load_name(self, state, name):
        value = await super().load_name(state, name)
        if value is not None:
            return value

        agent = AgentSynthesizerAgent(
            **AgentSynthesizerAgent.read_configuration_from_environment(environ),
        )

        response = agent.request(state)
        print("# {} {}".format(name, "#" * 80))
        print("{}".format(VirtualMachineStateRenderer().render(state)))
        print("#########")
        print(response.code)

        machine = VirtualMachine(VirtualMachineInlineHandler())

        sub_state = await machine.execute_string(
            response.code,
            symbol_loader=VirtualMachineDefaultSymbolLoader(),
            globals={
                "str": str,
                "dict": dict,
                "bool": bool,
                "int": int,
                "__annotations__": {},
                "print": print,
                "__module__": "main",
            },
        )

        async def wrapper(state, arguments, keyword_arguments):
            state = await sub_state.locals[name](sub_state, arguments, keyword_arguments)

            breakpoint()

            return state.transition(
                stack=[
                    *state.stack,
                    "Hello",
                ]
            )

        if "trace" not in state.context:
            state.context["trace"] = []

        state.context["trace"].append(
            {
                "name": name,
                "input_tokens": response.input_tokens,
                "output_tokens": response.output_tokens,
                "elapsed_time": response.elapsed_time,
            }
        )

        return VirtualMachineStateInlineCallable(wrapper)

def main():
    agent = HallucinatedWorkflowAgent(
        **HallucinatedWorkflowAgent.read_configuration_from_environment(environ),
    )

    while True:
        prompt = "Tell me a joke."#input("> ")

        #response = agent.request(prompt)

        code = """
joke: str = get_joke()
response: None = display_text(joke)
        """

        #code = response.code
        print(code)

        machine = VirtualMachine(
            VirtualMachineInlineHandler()
        )

        import dis

        state = run(
            machine.execute_string(
                code,
                symbol_loader=HallucinatedSymbolLoader(
                    allowed_imports=["typing"],
                ),
                globals={
                    "str": str,
                    "dict": dict,
                    "bool": bool,
                    "int": int,
                    "__annotations__": {},
                    "__module__": "main",
                },
                context={},
            )
        )

        if "trace" in state.context:
            for trace in state.context["trace"]:
                print(
                    "{} {} {} {}".format(
                        trace["name"],
                        trace["input_tokens"],
                        trace["output_tokens"],
                        trace["elapsed_time"],
                    )
                )

        break

if __name__ == "__main__":
    main()
