# AI Framework Comparison

Example implementations of a basic AI agent using different frameworks and approaches:
- Langchain Agent
- PydanticAI Agent

## Overview

This project involves implementations of a basic conversational AI agent which acts as a waiter at a restaurant, 
asking about dietary requirements and taking your order. 
They aim to demonstrate how the following features can be achieved with each approach:
- Human-in-the-loop input
- Tool calling with dependencies
- Conversation history/memory
- Structured outputs

## Requirements

- Python 3.11+
- API key for LLM provider (e.g., OpenAI, Anthropic, Gemini)

## Usage

1. Install from the repository:
```
pip install git@https://github.com/Finndersen/ai-framework-comparison.git
```

2. Run via CLI:
```
python -m ai_framework_comparison <framework> --model=<provider:model_name> --api_key=<api_key>
```

Run `python -m ai_framework_comparison -h` for details about the available options.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
