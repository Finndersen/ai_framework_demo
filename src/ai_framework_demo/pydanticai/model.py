from typing import cast

from pydantic_ai.models import KnownModelName, Model


def build_model_from_name_and_api_key(model_name: KnownModelName, api_key: str | None = None) -> Model:
    if model_name.startswith("openai:"):
        from pydantic_ai.models.openai import OpenAIModel

        return OpenAIModel(model_name[7:], api_key=api_key)

    elif model_name.startswith("anthropic:"):
        from pydantic_ai.models.anthropic import AnthropicModel

        return AnthropicModel(model_name[10:], api_key=api_key)

    elif model_name.startswith("google-gla:"):
        from pydantic_ai.models.gemini import GeminiModel, GeminiModelName

        return GeminiModel(cast(GeminiModelName, model_name[11:]), api_key=api_key)

    elif model_name.startswith("groq:"):
        from pydantic_ai.models.groq import GroqModel, GroqModelName

        return GroqModel(cast(GroqModelName, model_name[5:]), api_key=api_key)

    elif model_name.startswith("mistral:"):
        from pydantic_ai.models.mistral import MistralModel

        return MistralModel(model_name[8:], api_key=api_key)

    elif model_name.startswith("ollama:"):
        from pydantic_ai.models.ollama import OllamaModel

        return OllamaModel(model_name[7:], api_key=api_key or "ollama")

    else:
        raise ValueError(f"Unsupported model name: {model_name}")
