from . import OpenAIAgent
from datetime import datetime

class HallucinatedWorkflowAgentOutput:
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

class HallucinatedWorkflowAgent(OpenAIAgent):
    def request(self, task):
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
You are a workflow compiler that translates natural language tasks into executable Python 3 workflow plans.
Your job is to produce a high-level workflow expressed as valid Python 3 code.
The workflow must be sequential and explicit. Do not assume knowlege.

Wrap the entire output in a single Python code block exactly like this:
```python
<code>
```

Rules and constraints:
- The workflow must only contain function calls and variable assignments.
- Functions represent capabilities that will be implemented by separate agents at runtime.
- You must provide type annotations
- Do not implement or define the functions.
- Do not add imports, classes, comments or explanations.
- Do not output anything before or after the code block.
                    """.strip("\r\n ")
                },
                {
                    "role": "user",
                    "content": """
Task:
{}
                    """.format(task).strip("\r\n ")
                }
            ],
        )

        return HallucinatedWorkflowAgentOutput(
            HallucinatedWorkflowAgent.extract_block(
                completions.choices[0].message.content.strip("\n\r "),
                ["python", "python3"],
            ),
            datetime.now() - start,
            completions.usage.prompt_tokens,
            completions.usage.completion_tokens,
            completions.usage.total_tokens,
        )
