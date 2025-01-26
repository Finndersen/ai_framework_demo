import argparse

from pydantic_ai import Agent, RunContext
from pydantic_ai.messages import ModelMessage
from pydantic_ai.models import KnownModelName

from ai_framework_demo.llm import PROMPT_TEMPLATE, LLMResponse
from ai_framework_demo.pydanticai.deps import Dependencies
from ai_framework_demo.pydanticai.model import build_model_from_name_and_api_key
from ai_framework_demo.pydanticai.tools import create_order, get_menu
from ai_framework_demo.run_agent import AgentRunner
from ai_framework_demo.services import MenuService, OrderService


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


class PydanticAIAgentRunner(AgentRunner):
    agent: Agent[Dependencies, LLMResponse]
    deps: Dependencies
    message_history: list[ModelMessage]

    def __init__(self, menu_service: MenuService, order_service: OrderService, args: argparse.Namespace):
        self.agent = get_agent(model_name=args.model, api_key=args.api_key)
        self.deps = Dependencies(
            menu_service=menu_service,
            order_service=order_service,
            restaurant_name=args.restaurant_name,
            table_number=args.table_number,
        )
        self.message_history = []

    def make_request(self, user_message: str) -> LLMResponse:
        ai_response = self.agent.run_sync(
            user_message,
            deps=self.deps,
            message_history=self.message_history,
        )
        self.message_history = ai_response.all_messages()
        return ai_response.data
