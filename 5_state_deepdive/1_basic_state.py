from typing import TypedDict
from langgraph.graph import StateGraph, END


class SimpleSate(TypedDict):
    count: int


def increment(state: SimpleSate) -> SimpleSate:
    return {
        "count": state["count"] + 1
    }


graph = StateGraph(SimpleSate)

graph.add_node("increment",increment)

def should_continue(state: SimpleSate):
    if (state["count"] < 5):
        return "continue"
    return "stop"

graph.add_conditional_edges("increment", should_continue, {
    "continue": "increment",
    "stop": END
})

graph.set_entry_point("increment")

app = graph.compile()

# print(app.get_graph().draw_mermaid())

result = app.invoke({
    "count":0
})

print(result)