import argparse
from abc import ABC, abstractmethod

from rich.console import Console
from rich.live import Live
from rich.prompt import Prompt

from ai_framework_demo.llm import LLMResponse
from ai_framework_demo.services import MenuService, OrderService


class AgentRunner(ABC):
    """
    Base class which provides a common interface for initialising and making
    requests to an agent.
    """

    @abstractmethod
    def __init__(self, menu_service: MenuService, order_service: OrderService, args: argparse.Namespace): ...

    @abstractmethod
    def make_request(self, user_message: str) -> LLMResponse: ...


def run_agent(runner_class: type[AgentRunner], args: argparse.Namespace):
    """Initialise services and run agent conversation loop."""
    menu_service = MenuService()
    order_service = OrderService()

    agent_runner = runner_class(menu_service, order_service, args)
    user_message = "*Greet the customer*"
    console = Console()
    while True:
        with Live(console=console) as live_console:
            live_console.update("AI Waiter: ...")
            response = agent_runner.make_request(user_message)
            live_console.update(f"AI Waiter: {response.message}")

        # Exit if LLM indicates conversation is over
        if response.end_conversation:
            break

        user_message = Prompt.ask("You")

    # Show orders
    if orders := order_service.get_orders():
        console.print(f"Order placed: {orders}")
