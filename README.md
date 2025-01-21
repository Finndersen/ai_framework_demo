# AI Framework Comparison

A comparative analysis of Langchain and PydanticAI frameworks for building AI agents. This project demonstrates how to implement similar AI agent functionality using both frameworks, highlighting their unique approaches and trade-offs.

## Overview

This project implements parallel AI agents using:
- **Langchain**: A comprehensive framework for building LLM applications
- **PydanticAI**: A type-safe framework built on top of Pydantic for AI development

## Requirements

- Python 3.9+
- OpenAI API key

## Installation

1. Clone the repository:
```
git clone https://github.com/yourusername/ai-framework-comparison.git
cd ai-framework-comparison
```

2. Create and activate a virtual environment:
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the package with development dependencies:
```
make install
```

4. Set up your OpenAI API key:
```
export OPENAI_API_KEY=your_api_key_here
```

## Usage

Both implementations provide similar interfaces for easy comparison:

```python
from src.langchain.agent import LangchainAgent
from src.pydanticai.agent import PydanticAgent

# Using Langchain
langchain_agent = LangchainAgent()
result = await langchain_agent.process_query("What's the weather in London?")

# Using PydanticAI
pydantic_agent = PydanticAgent()
result = await pydantic_agent.process_query("What's the weather in London?")
```

## Development

This project uses modern Python development tools:

- **Ruff**: For linting and formatting
- **Pytest**: For testing
- **MyPy**: For type checking

Available commands:

```
make install  # Install development dependencies
make format   # Format code using ruff
make lint     # Run linters and type checking
make test     # Run tests
```

## Project Structure

```
ai_framework_comparison/
├── src/
│   ├── langchain/       # Langchain implementation
│   │   ├── __init__.py
│   │   └── agent.py
│   ├── pydanticai/      # PydanticAI implementation
│   │   ├── __init__.py
│   │   └── agent.py
│   ├── services.py      # Shared services
│   └── __init__.py
└── tests/               # Test suite
    ├── __init__.py
    ├── test_langchain_agent.py
    └── test_pydantic_agent.py
```

## Framework Comparison

### Langchain
**Pros**:
- Rich ecosystem of tools and integrations
- Built-in support for agents and chains
- Large community and extensive documentation
- Flexible architecture

**Cons**:
- Can be complex for simple use cases
- More boilerplate code required
- Steeper learning curve

### PydanticAI
**Pros**:
- Strong type safety through Pydantic
- Simple, intuitive API
- Less boilerplate code
- Familiar to Pydantic users

**Cons**:
- Newer framework with smaller ecosystem
- Fewer built-in tools and integrations
- Limited community resources

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linting (`make lint test`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
