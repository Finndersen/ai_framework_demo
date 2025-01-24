from pydantic_ai import Agent, RunContext
from pydantic_ai.models import KnownModelName

from ai_framework_demo.llm import PROMPT_TEMPLATE, LLMResponse
from ai_framework_demo.pydanticai.deps import Dependencies
from ai_framework_demo.pydanticai.tools import create_order, get_menu
from src.ai_framework_demo.pydanticai.model import build_model_from_name_and_api_key


def get_agent(model_name: KnownModelName, api_key: str | None = None) -> Agent[Dependencies, LLMResponse]:
    """
    Construct an agent with an LLM model, tools and system prompt
    """
    model = build_model_from_name_and_api_key(
        model_name=model_name,
        api_key=api_key,
    )
    # Tools can also be registered using @agent.tool decorator, but providing them like this is more appropriate when
    # constructing the agent dynamically
    agent = Agent(model=model, deps_type=Dependencies, tools=[get_menu, create_order], result_type=LLMResponse)

    # Define dynamic system prompt
    @agent.system_prompt
    def system_prompt(ctx: RunContext[Dependencies]) -> str:
        return PROMPT_TEMPLATE.format(restaurant_name=ctx.deps.restaurant_name, table_number=ctx.deps.table_number)

    return agent
