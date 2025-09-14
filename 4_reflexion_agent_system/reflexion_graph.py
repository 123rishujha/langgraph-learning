from typing import List
from langchain_core.messages import BaseMessage, ToolMessage
from langgraph.graph import MessageGraph, END
from chains import first_responder_chain, revisor_chain
from execute_tools import execute_tools
from pprint import pprint
import json


graph = MessageGraph()

graph.add_node("draft", first_responder_chain)
graph.add_node("execute_tools",execute_tools)
graph.add_node("revisor", revisor_chain)


graph.add_edge("draft", "execute_tools")
graph.add_edge("execute_tools", "revisor")

def event_loop(state: List[BaseMessage]) -> str:
    count_tool_visits = sum(isinstance(item, ToolMessage) for item in state)
    if count_tool_visits > 2:
        return END
    return "execute_tools"


graph.add_conditional_edges("revisor", event_loop, {
    END: END,
    "execute_tools": "execute_tools"
})


graph.set_entry_point("draft")

app = graph.compile()

res = app.invoke(
    "Write about how small bussiness can leverage ai to grow"
)
print("--------------- response -------------")
print( res)
print("\n-----------formatted-----------\n")
print(json.dumps([msg.dict() for msg in res],indent=2, ensure_ascii=False))
# print(app.get_graph().draw_mermaid())
# app.get_graph().print_ascii()
