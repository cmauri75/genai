from typing import TypedDict, List
from langgraph.graph import StateGraph

#State
class AgentState(TypedDict):
    values: List[int]
    operator: str
    name: str
    result: str

#node
def process_values(state: AgentState) -> AgentState:
    """Function processes multiple inputs and returns a result."""
    if 'operator' not in state.keys():
        state["result"] = f"Hello {state['name']} Operation on inputs: Invalid operator or empty values"
        return state

    if state["operator"] == "+":
        res = sum(state["values"])
    elif state["operator"] == "*":
        res = 1
        for value in state["values"]:
            res *= value
    state["result"] = f"Hello {state['name']} Operation on inputs: {res}"
    return state

graph = StateGraph(AgentState)
graph.add_node("processor",process_values)
graph.set_entry_point("processor")
graph.set_finish_point("processor")
app = graph.compile()

answer1 = app.invoke({"name": "Bob", "values": [2,3,4,5], "operator": "*"})
answer2 = app.invoke({"name": "Jon", "values": [2,3,4,5], "operator": "+"})
answer3 = app.invoke({"name": "Jak", "values": [2,3,4,5]})
print(answer1["result"])
print(answer2["result"])
print(answer3["result"])
