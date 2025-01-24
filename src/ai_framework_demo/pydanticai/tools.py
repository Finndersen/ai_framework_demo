from typing import Annotated

from pydantic_ai import RunContext

from ai_framework_demo.pydanticai.deps import Dependencies


def create_order(
    ctx: RunContext[Dependencies],
    table_number: int,
    order_items: Annotated[list[str], "List of food menu items to order"],
) -> str:
    """Create an order for the table"""
    ctx.deps.order_service.create_order(table_number, order_items)
    return "Order placed"


def get_menu(ctx: RunContext[Dependencies]) -> dict[str, list[str]]:
    """Get the full menu for the restaurant"""
    return ctx.deps.menu_service.get_menu()
