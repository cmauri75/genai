from typing import TypedDict, List
from langgraph.graph import StateGraph

#State
class AgentState(TypedDict):
    name: str
    age: str
    final: str

def first_node(state: AgentState) -> AgentState:
    """greets."""
    state["final"] = f"Hi {state['name']}"
    return state

def second_node(state: AgentState) -> AgentState:
    """get age."""
    state["final"] = f"You are  {state['age']} year old!"
    return state

graph = StateGraph(AgentState)
graph.add_node(first_node)
graph.add_node(second_node)
graph.set_entry_point("first_node")
graph.set_finish_point("second_node")
app = graph.compile()

res = app.invoke({"name": "Bob", "age": 23})

print(res)
