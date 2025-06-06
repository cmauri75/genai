from typing import TypedDict

from langgraph.graph import StateGraph


# State
class AgentState(TypedDict):
    name: str
    age: str
    final: str
    skills: list[str]


def first_node(state: AgentState) -> AgentState:
    """greets."""
    state["final"] = f"Hi {state['name']}"
    return state


def second_node(state: AgentState) -> AgentState:
    """get age."""
    state["final"] = state["final"] + " " + f"You are  {state['age']} year old!"
    return state

def third_node(state: AgentState) -> AgentState:
    """get skills."""
    state["final"] = state["final"] + " " + f"Your skills are {', '.join(state['skills'])}."
    return state

graph = StateGraph(AgentState)
graph.add_node(first_node)
graph.add_node(second_node)
graph.add_node(third_node)

graph.set_entry_point("first_node")
graph.add_edge("first_node", "second_node")
graph.add_edge("second_node", "third_node")
graph.set_finish_point("third_node")

app = graph.compile()

res = app.invoke({"name": "Bob", "age": 23, "skills": ["Python", "Java", "C++"]})

print(res)
