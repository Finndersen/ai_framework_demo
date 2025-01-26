from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel


def build_model_from_name_and_api_key(model_name: str, api_key: str | None = None) -> BaseChatModel:
    provider, model = model_name.split(":")
    api_key_arg_mapping = {
        "openai": "api_key",
        "anthropic": "api_key",
        "google-genai": "google_api_key",
    }
    init_kwargs = {api_key_arg_mapping[provider]: api_key} if api_key and provider in api_key_arg_mapping else {}
    return init_chat_model(model=model, model_provider=provider, **init_kwargs)  # type: ignore[call-overload]
