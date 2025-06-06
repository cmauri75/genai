from typing import Annotated, Sequence, TypedDict

from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, \
    HumanMessage, ToolMessage  # The foundational class for all message types in LangGraph
from langchain_core.messages import SystemMessage  # Message for providing instructions to the LLM
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

load_dotenv(dotenv_path="../../.env_secret")

# Global variable to hold the document content
document_content = ""


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


def agent(state: AgentState) -> AgentState:
    """
    Initialize the model
    """
    system_prompt = SystemMessage(
        content=f"""
    You are Drafter, a helpful writing assistant. You are going to help the user update and modify documents.
    
    - If the user wants to update or modify content, use the 'update' tool with the complete updated content.
    - If the user wants to save and finish, you need to use the 'save' tool.
    - Make sure to always show the current document state after modifications.
    
    The current document content is:{document_content}
    """)

    if not state["messages"]:
        user_input = "I'm ready to help you with your document. Please provide your instructions."
    else:
        user_input = input("\nPlease provide your instructions:")
        print(f"\n USER: {user_input}")
    user_message = HumanMessage(content=user_input)

    all_messages = [system_prompt] + list(state["messages"]) + [user_message]
    response = llm.invoke(all_messages)

    print(f"\nLLM: {response.content}")
    if hasattr(response, "tool_calls") and response.tool_calls:
        print(f"\nTool calls: {[tc['name'] for tc in response.tool_calls]}")

    return {"messages": list(state["messages"]) + [user_message, response]}


def should_continue(state: AgentState) -> bool:
    """
    Check if the agent should continue the conversation based on the last message's tool calls.
    """
    messages = state["messages"]
    if not messages:  # If there are no messages, we go on
        return True

    for message in reversed(messages):
        if (isinstance(message, ToolMessage) and
                "saved" in message.content.lower() and
                "document" in message.content.lower()):
            return False

    return True


@tool
def update(content: str) -> str:
    """Updates the document with provided content."""
    global document_content
    document_content = content
    return "Document updated successfully. New content is:\n" + document_content


@tool
def save(filename: str) -> str:
    """save the document to a file.
    Args:
        filename (str): The name of the file to save the document to.
    """
    global document_content
    if not document_content:
        return "Document is empty. Nothing to save."
    try:
        with open(filename, 'w') as file:
            file.write(document_content)
        return f"Document saved successfully to {filename}."
    except Exception as e:
        return f"Error saving document: {str(e)}"


tools = [update, save]
llm = ChatOpenAI(model="gpt-4.1-mini").bind_tools(tools)

tool_node = ToolNode(tools=tools)

graph = StateGraph(AgentState)
graph.add_node("agent", agent)
graph.add_node("tools", tool_node)

graph.set_entry_point("agent")
graph.add_edge("agent", "tools")
graph.add_conditional_edges(
    "tools",
    should_continue,
    {
        True: "agent",  # If the agent should continue, go back to the agent node
        False: END,  # If the agent should stop, go to the end node
    })

agent = graph.compile()

def print_messages(messages):
    """Function I made to print the messages in a more readable format"""
    if not messages:
        return
    for message in messages[-3:]:
        if isinstance(message, ToolMessage):
            print(f"\nTOOL RESULT: {message.content}")

def run_document_agent():
    print("\n ===== DRAFTER =====")

    state = {"messages": []}

    for step in agent.stream(state, stream_mode="values"):
        if "messages" in step:
            print_messages(step["messages"])

    print("\n ===== DRAFTER FINISHED =====")


if __name__ == "__main__":
    run_document_agent()
