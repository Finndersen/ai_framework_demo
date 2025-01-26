# AI Agent Framework Comparison

Example implementations of a basic conversational AI agent using different frameworks and approaches:
- [Langchain](https://github.com/langchain-ai/langchain) Agent
- [PydanticAI](https://github.com/pydantic/pydantic-ai) Agent

## Overview

This project includes implementations of a basic conversational AI agent which acts as a waiter at a restaurant, 
asking about dietary requirements and taking your order. 
They aim to demonstrate how the following features can be achieved with each approach:
- Dynamic model choice
- Human-in-the-loop input
- Tool calling with dependencies
- Conversation history/memory
- Dynamic system prompt
- Structured output

## Implementations
### Standard Agents
These approaches use PydanticAI's `Agent` and LangChain's legacy `AgentExecutor` classes to build the agent,
implementing the `AgentRunner` [common interface](./src/ai_framework_demo/run_agent.py). 

- PydanticAI implementation: [pydanticai/agent.py](./src/ai_framework_demo/pydantic_ai/agent.py)
- LangChain implementation: [langchain/agent.py](./src/ai_framework_demo/langchain/agent.py)

### Graph-based Agents

TBC

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
