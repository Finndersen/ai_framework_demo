from typing import Annotated

from langchain_core.tools import BaseTool, tool
from langgraph.prebuilt import InjectedState
from pydantic import BaseModel

from ai_framework_demo.llm import LLMResponse
from ai_framework_demo.services import MenuService, OrderService


# Define class-based tools to enable use of dependencies with legacy LangChain agents
class GetMenuTool(BaseTool):
    """
    Tool that can be used by the LLM to get the full menu for the restaurant.
    """

    name: str = "get_menu"
    description: str = "Get the full menu for the restaurant"
    menu_service: MenuService

    def _run(self) -> dict[str, list[str]]:
        return self.menu_service.get_menu()


class CreateOrderInputSchema(BaseModel):
    table_number: int
    order_items: Annotated[list[str], "List of food menu items to order"]


class CreateOrderTool(BaseTool):
    """
    Tool that can be used by the LLM to create an order for the table.
    """

    name: str = "create_order"
    description: str = "Create an order for the table"
    args_schema: type[BaseModel] = CreateOrderInputSchema
    order_service: OrderService

    def _run(self, table_number: int, order_items: list[str]) -> str:
        self.order_service.create_order(table_number, order_items)
        return "Order placed"


class StructuredResponseTool(BaseTool):
    """
    Tool that can be used by the LLM to provide a structured response to the user.
    Does not have any associated functionality, it is just a way to enable structured output from the LLM.
    """

    name: str = "respond_to_user"
    description: str = (
        "ALWAYS use this tool to provide a response to the user, INSTEAD OF responding directly. "
        "The `message` content should be what you would normally respond with in a conversation. "
        "The `end_conversation` flag should be set to True if the conversation should end after this response."
    )
    args_schema: type[BaseModel] = LLMResponse

    # The following content is only used by legacy AgentExecutor, not required for graph agent
    return_direct: bool = True  # Causes the tool result to be returned directly to the user

    def _run(self, message: str, end_conversation: bool) -> str:
        # Return a serialised str as a workaround to avoid a validation error in the RunnableWithMessageHistory
        return LLMResponse(message=message, end_conversation=end_conversation).model_dump_json()


# Function-based tools with dependency injection using InjectedState with Langgraph
@tool
def get_menu(menu_service: Annotated[MenuService, InjectedState("menu_service")]) -> dict[str, list[str]]:
    """Get the full menu for the restaurant"""
    return menu_service.get_menu()


@tool
def create_order(
    order_service: Annotated[OrderService, InjectedState("order_service")],
    table_number: int,
    order_items: Annotated[list[str], "List of food menu items to order"],
) -> str:
    """Create an order for the table"""
    order_service.create_order(table_number, order_items)
    return "Order placed"
