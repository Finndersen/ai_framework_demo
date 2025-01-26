import argparse

from langchain_core.messages import HumanMessage
from langchain_core.messages.ai import AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import END, MessagesState, StateGraph
from langgraph.prebuilt.tool_node import ToolNode

from ai_framework_demo.langchain.model import build_model_from_name_and_api_key
from ai_framework_demo.langchain.tools import StructuredResponseTool, create_order, get_menu
from ai_framework_demo.llm import PROMPT_TEMPLATE, LLMResponse
from ai_framework_demo.services import MenuService, OrderService


class AgentState(MessagesState):
    """Custom agent state object with dependencies.
    This is what will be passed through each node of the graph"""

    menu_service: MenuService
    order_service: OrderService
    restaurant_name: str
    table_number: int
    final_response: LLMResponse | None


def get_agent_graph(model_name: str, api_key: str | None = None) -> StateGraph:
    """
    Build an agent graph that handles the cycle of LLM invocation and tool calling,
    as well as returning a structured response to the user
    """
    model = build_model_from_name_and_api_key(
        model_name=model_name,
        api_key=api_key,
    )
    structured_response_tool = StructuredResponseTool()

    # Register the StructuredResponseTool tool to enable structured output
    tools = [get_menu, create_order, structured_response_tool]

    model_with_tools = model.bind_tools(tools, tool_choice=True)
    # Define a custom prompt template that will be used to insert the dynamic system prompt before passing to the LLM
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", PROMPT_TEMPLATE),
            ("placeholder", "{messages}"),
        ]
    )

    # Create a chain with the prompt pre-processor and the model with tools
    model_with_prompt = prompt | model_with_tools

    # Define the grpah node function for calling the model
    def call_model(state: AgentState):
        # print("calling model with state: ", state)
        response = model_with_prompt.invoke(state)  # type: ignore[arg-type]
        # Return response as a message list to be appended to the message history
        return {"messages": [response]}

    # Define the graph node function that builds the final structured response to the user
    # This is done automatically by model.with_structured_output(), but that can't be used with other tools
    def respond(state: AgentState):
        # Construct the final answer from the arguments of the last tool call
        llm_response_message = state["messages"][-1]
        assert isinstance(llm_response_message, AIMessage)

        structured_response_tool_call = llm_response_message.tool_calls[0]
        response = LLMResponse(**structured_response_tool_call["args"])
        # Since we're using tool calling to return structured output,
        # we need to add  a tool message corresponding to the LLMResult tool call,
        # This is due to LLM providers' requirement that AI messages with tool calls
        # need to be followed by a tool message for each tool call
        tool_message = {
            "type": "tool",
            "content": "*message displayed to user*",
            "tool_call_id": structured_response_tool_call["id"],
            "name": structured_response_tool.name,  # Gemini (and maybe others) causes error if name is not set
        }
        # We return the final answer
        return {"final_response": response, "messages": [tool_message]}

    # Define the graph edge function that determines whether to continue processing tool calls,
    # or to respond to the user with a structured response
    def should_continue(state: AgentState):
        last_message = state["messages"][-1]
        assert isinstance(last_message, AIMessage)

        # If there is only one tool call and it is the response tool call we respond to the user
        if len(last_message.tool_calls) == 1 and last_message.tool_calls[0]["name"] == structured_response_tool.name:
            return "respond"
        # Otherwise we will use the tool node again
        else:
            return "continue"

    # Define a new graph
    workflow = StateGraph(AgentState)

    # Define the two nodes we will cycle between
    workflow.add_node("agent", call_model)
    workflow.add_node("respond", respond)
    workflow.add_node("tools", ToolNode(tools))

    # Set the entrypoint as `agent`
    # This means that this node is the first one called
    workflow.set_entry_point("agent")

    # We now add a conditional edge
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "continue": "tools",
            "respond": "respond",
        },
    )

    workflow.add_edge("tools", "agent")
    workflow.add_edge("respond", END)

    return workflow


def run_langgraph_agent(args: argparse.Namespace):
    agent_graph = get_agent_graph(model_name=args.model, api_key=args.api_key).compile()

    # Initialize services
    menu_service = MenuService()
    order_service = OrderService()

    # Initialise graph state
    state = AgentState(
        menu_service=menu_service,
        order_service=order_service,
        restaurant_name=args.restaurant_name,
        table_number=args.table_number,
        messages=[HumanMessage(content="*Greet the customer*")],
        final_response=None,
    )

    while True:
        response_state = agent_graph.invoke(state)
        print(response_state["messages"])
        final_response: LLMResponse = response_state["final_response"]
        print("AI Waiter:", final_response.message)

        if final_response.end_conversation:
            break

        user_message = input("You: ")

        # Add user message to the message history
        state["messages"] = response_state["messages"] + [HumanMessage(content=user_message)]
        print(state["messages"])

    # Show orders
    if orders := order_service.get_orders():
        print("Order placed: ", orders)
