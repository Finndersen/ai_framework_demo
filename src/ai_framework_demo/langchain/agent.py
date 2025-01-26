import argparse
from collections.abc import Sequence

from langchain.agents.agent import AgentExecutor
from langchain.agents.format_scratchpad.tools import format_to_tool_messages
from langchain.agents.output_parsers.tools import ToolsAgentOutputParser
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables.config import RunnableConfig
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.tools import BaseTool

from ai_framework_demo.langchain.model import build_model_from_name_and_api_key
from ai_framework_demo.langchain.tools import (
    CreateOrderTool,
    GetMenuTool,
    StructuredResponseTool,
)
from ai_framework_demo.llm import PROMPT_TEMPLATE, LLMResponse
from ai_framework_demo.run_agent import AgentRunner
from ai_framework_demo.services import MenuService, OrderService


def get_agent_executor(
    tools: Sequence[BaseTool], model_name: str, api_key: str | None = None
) -> RunnableWithMessageHistory:
    """
    Construct an agent with an LLM model, tools and system prompt
    """
    model = build_model_from_name_and_api_key(
        model_name=model_name,
        api_key=api_key,
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                PROMPT_TEMPLATE,
            ),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )

    # Re-implement create_tool_calling_agent() here, but force tool use
    llm_with_tools = model.bind_tools(tools, tool_choice=True)
    agent = (
        RunnablePassthrough.assign(agent_scratchpad=lambda x: format_to_tool_messages(x["intermediate_steps"]))
        | prompt
        | llm_with_tools
        | ToolsAgentOutputParser()
    )

    agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools)

    # Enable chat history/memory (very convoluted)
    # Use a single message history (no need for multiple threads)
    message_history = ChatMessageHistory()

    agent_with_chat_history = RunnableWithMessageHistory(
        runnable=agent_executor,  # type: ignore[arg-type]
        get_session_history=lambda _: message_history,
        input_messages_key="input",
        history_messages_key="chat_history",
    )

    return agent_with_chat_history


class LangchainAgentRunner(AgentRunner):
    def __init__(self, menu_service: MenuService, order_service: OrderService, args: argparse.Namespace):
        # Initialise tools with dependencies
        tools = [
            GetMenuTool(menu_service=menu_service),
            CreateOrderTool(order_service=order_service),
            StructuredResponseTool(),
        ]
        self.agent_executor = get_agent_executor(tools=tools, model_name=args.model, api_key=args.api_key)
        self.static_input_content = {"restaurant_name": args.restaurant_name, "table_number": args.table_number}
        self.config: RunnableConfig = {"configurable": {"session_id": "not-even-used"}}

    def make_request(self, user_message: str) -> LLMResponse:
        result = self.agent_executor.invoke(self.static_input_content | {"input": user_message}, self.config)
        # De-serialise structured response into an LLMResponse
        response = LLMResponse.model_validate_json(result["output"])
        return response
