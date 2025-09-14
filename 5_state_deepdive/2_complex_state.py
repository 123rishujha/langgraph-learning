from langgraph.graph import StateGraph, END
from typing import TypedDict,List

class SimpleState(TypedDict):
    count: int
    sum: int
    history: List[int]


def increment(state: SimpleState)-> SimpleState:
    updated_count = state["count"]+1 
    return {
        "count": updated_count,
        "sum": state["sum"] + updated_count,
        "history": state["history"] + [updated_count]
    }

graph = StateGraph(SimpleState)

graph.add_node("increment", increment)

def should_continue(state: SimpleState) -> SimpleState:
    if (state["count"] < 5):
        return "continue"
    return "stop"


graph.add_conditional_edges("increment", should_continue, {
    "continue": "increment",
    "stop": END
})

graph.set_entry_point("increment")
app =  graph.compile()

result = app.invoke({
    "count":0,
    "sum":0,
    "history":[],
})

print(result)
