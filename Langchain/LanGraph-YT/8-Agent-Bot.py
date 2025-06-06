from typing import TypedDict, Union

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph

load_dotenv(dotenv_path="../../.env_secret", verbose=True)
llm = ChatOpenAI(model="gpt-4.1-nano", temperature=0.0, max_tokens=1000)


class AgentState(TypedDict):
    message_chain: list[Union[HumanMessage, AIMessage]] ## Union allows for both HumanMessage and AIMessage types in the list

def processor(state: AgentState) -> AgentState:
    """
    Process all old input messages, ask LLM and add to chain.
    """
    response = llm.invoke(state["message_chain"])
    print(f"Response: {response.content}")
    state["message_chain"].append(AIMessage(content=response.content))
    return state


graph = StateGraph(AgentState)
graph.add_node(processor)
graph.set_entry_point("processor")
graph.set_finish_point("processor")
agent = graph.compile()

conversation_history = []

user_input = input("Enter your message: ")
while user_input != "quit":
    conversation_history.append(user_input)
    state = agent.invoke({"message_chain": conversation_history})
    conversation_history = state["message_chain"]
    user_input = input("Enter your message: ")
