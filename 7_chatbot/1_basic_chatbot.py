from typing import TypedDict, Annotated
from langgraph.graph import StateGraph,add_messages, END
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()

llm = ChatGroq(model="llama-3.1-8b-instant")


class BasicChatState(TypedDict):
    messages: Annotated[list,add_messages]

def chatbot(state: BasicChatState):
    return {
        "messages": [llm.invoke(state["messages"])]
    }

graph = StateGraph(BasicChatState)

graph.add_node("chatbot", chatbot)
graph.add_edge("chatbot",END)
graph.set_entry_point("chatbot")

app = graph.compile()

while True:
    user_input = input("User: ")
    if(user_input in ['exit','end']):
        break
    result = app.invoke({
        "messages": [HumanMessage(content=user_input)]
    })
    print("------------result:-------- \n",result)
