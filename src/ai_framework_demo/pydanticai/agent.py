from dataclasses import dataclass
from typing import cast

from pydantic_ai import Agent, RunContext
from pydantic_ai.models import KnownModelName, Model

from ai_framework_demo.prompt import PROMPT_TEMPLATE
from ai_framework_demo.services import MenuService, OrderService


@dataclass
class Dependencies:
    menu_service: MenuService
    order_service: OrderService
    restaurant_name: str
    table_number: int


def get_agent(model: Model) -> Agent[Dependencies, str]:
    agent = Agent(
        model=model,
        deps_type=Dependencies,
    )

    # Define dynamic system prompt
    @agent.system_prompt
    def system_prompt(ctx: RunContext[Dependencies]) -> str:
        return PROMPT_TEMPLATE.format(restaurant_name=ctx.deps.restaurant_name, table_number=ctx.deps.table_number)

    # Define tools (can also be provided as a list of functions when initializing the agent)
    @agent.tool
    def get_menu(ctx: RunContext[Dependencies]) -> dict[str, list[str]]:
        """Get the full menu for the restaurant"""
        return ctx.deps.menu_service.get_menu()

    @agent.tool
    def create_order(ctx: RunContext[Dependencies], table_number: int, order_items: list[str]) -> str:
        """Create an order for the table"""
        ctx.deps.order_service.create_order(table_number, order_items)
        return "Order placed"

    return agent


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
