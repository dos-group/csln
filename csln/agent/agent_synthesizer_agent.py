from . import OpenAIAgent
from ..virtual_machine import VirtualMachineStateRenderer
from datetime import datetime

class AgentSynthesizerAgentOutput:
    def __init__(self, code, elapsed_time, input_tokens, output_tokens, total_tokens):
        self.__code = code
        self.__elapsed_time = elapsed_time
        self.__input_tokens = input_tokens
        self.__output_tokens = output_tokens
        self.__total_tokens = total_tokens

    @property
    def code(self):
        return self.__code

    @property
    def elapsed_time(self):
        return self.__elapsed_time

    @property
    def input_tokens(self):
        return self.__input_tokens

    @property
    def output_tokens(self):
        return self.__output_tokens

    @property
    def total_tokens(self):
        return self.__total_tokens


class AgentSynthesizerAgent(OpenAIAgent):
    def request(self, state):
        options = {}

        if self.model_temperature is not None:
            options["temperature"] = self.model_temperature

        start = datetime.now()

        completions = self.client.chat.completions.create(
            model=self.model_name,
            **options,
            messages=[
                {
                    "role": "system",
                    "content": """
You are an execution agent that generates Python 3 functions for high-level workflow steps.
You will receive the workflow step that must be executed, the function name, the input parameters
and the expected return value. Your task is to generate a Python 3 function implementation
that fulfills the requested capability.

Output format:
```python
<code>
```

Rules and constraints:
- Only implement the requested function.
- The function name and parameters MUST match exactly.
- The function must return the requested output.
- The function should try to solve the task autonomously.
- The function may call helper tools if needed.
- The function must be safe and deterministic.
- The function must contain valid Python 3 code.
- Do not include explanations.
- Do not include any text outside the Python code block.

                    """.strip("\r\n ")
                },
                {
                    "role": "user",
                    "content": """
State:
{}

Function Name:
{}
                    """.format(
                        VirtualMachineStateRenderer().render(state),
                        state.current_instruction_argument_value,
                    ).strip("\r\n ")
                }
            ],
        )

        return AgentSynthesizerAgentOutput(
            AgentSynthesizerAgent.extract_block(
                completions.choices[0].message.content.strip("\n\r "),
                ["python", "python3"],
            ),
            datetime.now() - start,
            completions.usage.prompt_tokens,
            completions.usage.completion_tokens,
            completions.usage.total_tokens,
        )
