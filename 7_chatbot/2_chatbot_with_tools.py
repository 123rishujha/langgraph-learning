from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END, add_messages
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage,AIMessage
from langgraph.prebuilt import ToolNode


class BasicChatBot(TypedDict):
    messages: Annotated[list,add_messages]

llm = ChatGroq(model="llama-3.1-8b-instant")

tavily_search = TavilySearchResults(max_results=2)

tools = [tavily_search]

llm_with_tools = llm.bind_tools(tools=tools)

def chat_node(state: BasicChatBot):
    return {
        "messages": [llm_with_tools.invoke(state["messages"])]
    }

def tool_router(state: BasicChatBot):
    last_msg = state["messages"][-1]
    if(hasattr(last_msg, "tool_calls") and len(last_msg.tool_calls) > 0):
        return "tool_node"
    else:
        return END



tool_node = ToolNode(tools=tools)

graph = StateGraph(BasicChatBot)

graph.add_node("chat_node",chat_node)
graph.add_node("tool_node",tool_node)

graph.add_conditional_edges("chat_node",tool_router)
graph.add_edge("tool_node","chat_node")


graph.set_entry_point("chat_node")

app = graph.compile()

while True:
    user_input = input("User: ")
    if(user_input in ["end","exit"]):
        break
    else:
        result = app.invoke({
            "messages": [HumanMessage(content=user_input)]
        })
        print("\n------------- result----------------\n")
        print(result)

