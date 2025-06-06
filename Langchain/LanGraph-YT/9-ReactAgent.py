from typing import Annotated, Sequence, TypedDict

from dotenv import load_dotenv
from langchain_core.messages import BaseMessage  # The foundational class for all message types in LangGraph
from langchain_core.messages import SystemMessage  # Message for providing instructions to the LLM
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

load_dotenv(dotenv_path="../../.env_secret")


class AgentState(TypedDict):
    """
    Annotated: add metadata to a variable
     Sequence: is a list of items
     BaseMessage: is the main message type in LangGraph
     add_messages: add a message to list, if id is the same on an existing message, it will update that message
    """
    messages: Annotated[Sequence[BaseMessage], add_messages]


def model_call(state: AgentState) -> AgentState:
    """
    Initialize the model
    """
    system_prompt = SystemMessage(
        content="You are my AI assistant. Please respond to the user's requests and use tools when necessary. ")
    response = llm.invoke(
        [system_prompt] + state["messages"])  # Invoke the model with the system prompt and the conversation history
    return {"messages":
                [response]}  # NB: the reduce function "add_messages" is used to combine the messages into original list


def should_continue(state: AgentState) -> bool:
    """
    Check if the agent should continue
    """
    messages = state["messages"]
    last_message = messages[-1]
    if not last_message.tool_calls:  # If the last message has no tool calls, we can stop
        return False
    else:
        return True


def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()


@tool
def a_stop(a: int, b: int) -> int:
    """a_stop two numbers"""
    print("*** called add tool", a, b)
    return a + b + 1


@tool
def s_stop(a: int, b: int) -> int:
    """s_stop two numbers"""
    print("*** called subtract tool", a, b)
    return a - b + 1


@tool
def m_stop(a: int, b: int) -> int:
    """m_stop two numbers"""
    print("**** called multiply tool", a, b)
    return a * b +1


tools = [a_stop, s_stop, m_stop]
llm = ChatOpenAI(model="gpt-4.1-mini").bind_tools(tools)
# Better results are obtained with gpt-4.1

tool_node = ToolNode(tools=tools)

graph = StateGraph(AgentState)
graph.add_node("agent", model_call)
graph.add_node("tool_node", tool_node)

graph.set_entry_point("agent")
graph.add_conditional_edges(
    "agent",
    should_continue,
    {
        True: "tool_node",  # If the agent should continue, go back to the agent node
        False: END,  # If the agent should stop, go to the end node
    })
graph.add_edge("tool_node", "agent")

agent = graph.compile()

inputs = {"messages": [("user",  "a_stop 5 and 5, then apply s_stop between last operation result and 10. At last m_stop by 3")]}
print_stream(
    agent.stream(inputs, stream_mode="values"))  # Initial input to the agent, a user message asking to add two numbers
