import argparse

import logfire
from pydantic_ai.messages import ModelMessage

from ai_framework_demo.pydanticai.agent import (
    get_agent,
)
from ai_framework_demo.pydanticai.deps import Dependencies
from ai_framework_demo.services import MenuService, OrderService


def run_pydanticai(args: argparse.Namespace):
    logfire.configure(send_to_logfire="if-token-present", console=None if args.debug else False)

    agent = get_agent(model_name=args.model, api_key=args.api_key)

    # Initialize services
    menu_service = MenuService()
    order_service = OrderService()

    # Run agent with dependencies
    deps = Dependencies(
        menu_service=menu_service,
        order_service=order_service,
        restaurant_name=args.restaurant_name,
        table_number=args.table_number,
    )

    message_history: list[ModelMessage] = []
    user_message = "*Greet the customer*"

    while True:
        ai_response = agent.run_sync(
            user_message,
            deps=deps,
            message_history=message_history,
        )
        message_history = ai_response.all_messages()
        print("AI Waiter: ", ai_response.data.message)

        # Exit if LLM indicates conversation is over
        if ai_response.data.end_conversation:
            break

        user_message = input("You: ")

    # Show orders
    if orders := order_service.get_orders():
        print("Order placed: ", orders)
