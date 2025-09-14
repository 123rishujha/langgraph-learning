from dotenv import load_dotenv
load_dotenv()
from typing import TypedDict, Annotated
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END, add_messages
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage

CHAT_NODE = "CHAT_NODE"

class BasicChatState(TypedDict):
    messages: Annotated[list, add_messages]

llm = ChatGroq(model="llama-3.1-8b-instant")

memory = MemorySaver()

def chat_node(state: BasicChatState):
    return {
        "messages": [llm.invoke(state["messages"])]
    }


graph = StateGraph(BasicChatState)

graph.add_node(CHAT_NODE, chat_node)
graph.add_edge(CHAT_NODE, END)

graph.set_entry_point(CHAT_NODE)

app = graph.compile(checkpointer=memory)

config = {
    "configurable": {
        "thread_id": 1
    }
}

while True:
    user_input = input("User: ")
    if(user_input in ["exit","end"]):
        break
    else:
        result = app.invoke({
            "messages": [HumanMessage(content=user_input)]
        }, config=config)
        print("-------------------------- result -------------------------")
        # print(result)
        print(result["messages"][-1].content)

