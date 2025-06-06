from typing import TypedDict

from langgraph.graph import StateGraph, START, END


# State
class AgentState(TypedDict):
    number1: int
    number2: int
    operator: str
    finalNumber: int

def adder(state: AgentState) -> AgentState:
    """adds two numbers"""
    state["finalNumber"] = state["number1"] + state["number2"]
    return state

def subtractor(state: AgentState) -> AgentState:
    """subtracts two numbers"""
    state["finalNumber"] = state["number1"] - state["number2"]
    return state


def decide_next_node(state: AgentState) -> str:
    """this node decides which node to go next based on the operator"""
    if state["operator"] == "+":
        return "add"
    elif state["operator"] == "-":
        return "sub"
    else:
        return "END"  # If operator is not recognized, end the graph


graph = StateGraph(AgentState)
graph.add_node("router",lambda state: state)  # This node just passes the state to the next node
graph.add_node(adder)
graph.add_node(subtractor)

graph.add_edge(START, "router")
graph.add_conditional_edges("router", decide_next_node, {
    #"edge : node" format
    "add": "adder",
    "sub": "subtractor",
    "END": END
})
graph.add_edge("adder", END)
graph.add_edge("subtractor", END)

app = graph.compile()

res = app.invoke({"number1": 5, "number2": 3, "operator": "+"})
res2 = app.invoke({"number1": 5, "number2": 3, "operator": "-"})
res3 = app.invoke({"number1": 5, "number2": 3, "operator": "*"})

print(res)
print(res2)
print(res3)
