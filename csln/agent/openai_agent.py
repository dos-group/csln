from openai import (
    OpenAI,
    AzureOpenAI,
)

class OpenAIAgent:
    def __init__(
            self,
            model_url,
            model_key,
            model_name,
            model_temperature = None,
            azure_client = False,
    ):
        self.__azure_client = azure_client
        self.__model_url = model_url
        self.__model_key = model_key
        self.__model_name = model_name
        self.__model_temperature = model_temperature

        options = {}

        if model_key is not None:
            options["api_key"] = model_key

        if azure_client is True:
            if model_url is not None:
                options["azure_endpoint"] = model_url

            self.__client = AzureOpenAI(
                api_version="2024-07-01-preview",
                **options,
            )
        else:
            if model_url is not None:
                options["base_url"] = model_url

            self.__client = OpenAI(
                **options,
            )

    @staticmethod
    def read_configuration_from_environment(environment, prefix=None):
        if prefix is None:
            prefix = ""

        model_name = environment.get(f"{prefix}MODEL_NAME", None)
        model_url = environment.get(f"{prefix}MODEL_URL", None)

        if model_name is None:
            return None

        if model_url is None:
            return None

        configuration = {
            "model_name": model_name,
            "model_url": model_url,
        }

        model_key = environment.get(f"{prefix}MODEL_KEY", None)
        if model_key is not None:
            configuration["model_key"] = model_key

        azure_client = environment.get(f"{prefix}AZURE_CLIENT", None)
        if azure_client is not None:
            configuration["azure_client"] = azure_client.lower() in ["true", "t", "1", "on"]

        model_temperature = environment.get(f"{prefix}MODEL_TEMPERATURE", None)
        if model_temperature is not None:
            configuration["model_temperature"] = float(model_temperature)

        return configuration

    @staticmethod
    def extract_block(output, marker_names):
        marker = "```"

        left_markers = [
            marker,
            *map(
                lambda marker_name: "{}{}".format(marker_name, marker),
                marker_names,
            ),
            *map(
                lambda marker_name: "{}{}".format(marker, marker_name),
                marker_names,
            ),
        ]

        right_marker = marker

        output = output.strip("\n\r ")

        start = None
        start_padding = None

        for left_marker in left_markers:
            index = output.find(left_marker)

            if index < 0:
                continue

            if start_padding is not None and len(left_marker) < start_padding:
                continue

            start = index
            start_padding = len(left_marker)

        if start is None:
            return None

        end = output.find(right_marker, start + start_padding)
        if end < 0:
            end = len(output)

        if end is None:
            return None

        return output[start + start_padding:end].strip("\n\r ")

    @property
    def client(self):
        return self.__client

    @property
    def azure_enabled(self):
        return self.__azure_enabled

    @property
    def model_url(self):
        return self.__model_url

    @property
    def model_key(self):
        return self.__model_key

    @property
    def model_name(self):
        return self.__model_name

    @property
    def model_temperature(self):
        return self.__model_temperature
