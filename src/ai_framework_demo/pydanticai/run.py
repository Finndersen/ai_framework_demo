import argparse

import logfire

from ai_framework_demo.pydanticai.agent import (
    Dependencies,
    build_model_from_name_and_api_key,
    get_agent,
)
from ai_framework_demo.services import MenuService, OrderService


async def run_pydanticai(args: argparse.Namespace):
    logfire.configure(send_to_logfire="if-token-present", console=None if args.debug else False)

    model = build_model_from_name_and_api_key(
        model_name=args.model,
        api_key=args.api_key,
    )

    agent = get_agent(model)

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

    greeting_response = await agent.run(
        "*Greet the customer*",
        deps=deps,
    )

    message_history = greeting_response.all_messages()
    print("AI Waiter: ", greeting_response.data)
    while True:
        user_input = input("You: ")
        ai_response = await agent.run(
            user_input,
            deps=deps,
            message_history=message_history,
        )
        print("AI Waiter: ", ai_response.data)

        message_history = ai_response.all_messages()
        # Exit if order has been placed
        if orders := order_service.get_orders():
            print("Order placed: ", orders)
            break
