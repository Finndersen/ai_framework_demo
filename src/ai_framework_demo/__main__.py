import argparse
import os
from collections import defaultdict
from typing import Literal, cast, get_args

import logfire
from pydantic_ai.models import KnownModelName

from ai_framework_demo.pydanticai.agent import PydanticAIAgentRunner
from ai_framework_demo.run_agent import run_agent

FrameworkChoice = Literal["langchain", "pydanticai"]


def format_model_options() -> str:
    # Group models by provider
    grouped: defaultdict[str, list[str]] = defaultdict(list)
    for item in cast(tuple[KnownModelName], get_args(KnownModelName)):
        if item == "test" or item.startswith("google-vertex"):
            continue
        provider, model = item.split(":")
        grouped[provider].append(model)

    # Format the output
    formatted_lines = [f"- {provider}: {', '.join(models)}" for provider, models in grouped.items()]
    return "\n".join(formatted_lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="AI Framework Demo - Compare Langchain and PydanticAI implementations")

    parser.add_argument(
        "framework",
        type=str,
        choices=["langchain", "pydanticai"],
        default="pydanticai",
        help="Which framework to use (default: pydanticai)",
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode",
    )

    parser.add_argument(
        "--model",
        type=str,
        default="openai:gpt-4-turbo-preview",
        help="Name of the LLM model to use, in format provider:model (e.g. openai:gpt-4). "
        "Choices (not exhaustive, more may be supported):\n" + format_model_options(),
        metavar="PROVIDER:MODEL",
        # Don't strictly enforce choices since new models may be added
    )

    parser.add_argument(
        "--api-key",
        type=str,
        default=None,
        required=False,
        help="API key for the model service. If not provided, will look for OPENAI_API_KEY environment variable",
    )

    parser.add_argument(
        "--restaurant-name",
        type=str,
        default="Le Bistro",
        help="Name of the restaurant (default: Le Bistro)",
    )

    parser.add_argument(
        "--table-number",
        type=int,
        default=1,
        help="Table number for the order (default: 1)",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    # Get API key from args or environment
    api_key = args.api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "API key must be provided either via --api-key argument or OPENAI_API_KEY environment variable"
        )

    if args.framework == "pydanticai":
        logfire.configure(send_to_logfire="if-token-present", console=None if args.debug else False)
        run_agent(PydanticAIAgentRunner, args)
    else:
        raise ValueError(f"Invalid framework: {args.framework}")


if __name__ == "__main__":
    main()
