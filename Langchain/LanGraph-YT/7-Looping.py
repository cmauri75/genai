import random
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# State
class AgentState(TypedDict):
    username: str
    numbers: list[int]
    counter: int


def greeter(state: AgentState) -> AgentState:
    """greets the user"""
    state["username"] = f"Hello {state['username']}, welcome to the random number generator!"
    state["counter"] = 0
    return state


def randomGenerator(state: AgentState) -> AgentState:
    """generates a random number between two numbers and appends it to the list"""
    state["numbers"].append(random.randint(0, 10))
    state["counter"] += 1
    return state


def should_continue(state: AgentState) -> bool:
    """checks if the user wants to continue"""
    print("Loop: ", state["counter"])
    return state["counter"] < 5

graph = StateGraph(AgentState)
graph.add_node(greeter)
graph.add_node(randomGenerator)

graph.add_edge(START, "greeter")
graph.add_edge("greeter", "randomGenerator")

graph.add_conditional_edges("randomGenerator", should_continue, {
    True: "randomGenerator",
    False: END
})

app = graph.compile()
res = app.invoke({"username": "Bog", "numbers": []})
print(res)
