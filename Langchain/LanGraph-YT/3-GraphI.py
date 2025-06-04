#Helloworld graph

from typing import TypedDict, Dict
from langgraph.graph import StateGraph
from rich.jupyter import display


# Shared data structure that keeps track of the state of the agent while application is running
class AgentState(TypedDict):
    message: str

# node, input and output are the state of the agent
def greeting_node(state: AgentState) -> AgentState:
    #Doc String, important for documentation and understanding the code, it tells what the function does
    """A node that sets a greeting message in the state."""
    state["message"] = "Hello "+state["message"]+", how do you do?"
    return state

#Create the graph
graph = StateGraph(AgentState)

#Add nodes
graph.add_node("greeter",greeting_node)

#define start and end points of the graph
graph.set_entry_point("greeter")
graph.set_finish_point("greeter")

#compiles the graph, this is necessary to check for errors and prepare the graph for execution
app = graph.compile()

print(app.config_specs)

from IPython.display import Image

Image(app.get_graph().draw_mermaid_png())

app.invoke({"message": "Bob"})  # Invoke the graph with an initial state
