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

## Example Conversation

> **AI Waiter:** Ah, bonjour madame et monsieur! Welcome to Le Bistro, where the food is as delightful as the company! Before we embark on a culinary adventure, might you have any dietary restrictions or preferences? We wouldn't want any rogue ingredients crashing the party!

> **You:** I only eat yellow coloured food

> **AI Waiter:** Magnifique! A connoisseur of the golden hue, I see! Let's explore the menu with your sunshine-filled preference in mind. For appetizers, we have the Quinoa Stuffed Bell Peppers, which are a vibrant yellow. For the main course, the Chickpea and Sweet Potato Curry is a golden delight! And for 
dessert, the Fresh Fruit Sorbet might have some yellow options depending on the day! What do you think?

> **You:** I'll take the Bell Peppers and fruit sorbet thanks

> **AI Waiter:** Excellent choices! One order of the Quinoa Stuffed Bell Peppers and the Fresh Fruit Sorbet for the discerning palate at table number 1! Your order has been placed, and I shall return with your delectable delights shortly. Au revoir!

> **Order placed:** [Order(menu_items=['Quinoa Stuffed Bell Peppers', 'Fresh Fruit Sorbet'], table_number=1)]


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
