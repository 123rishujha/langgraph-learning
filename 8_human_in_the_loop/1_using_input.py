from dotenv import load_dotenv
load_dotenv()
from langgraph.graph import StateGraph, END, add_messages
from langchain_core.messages import HumanMessage
from typing import TypedDict, Annotated
from langchain_groq import ChatGroq


# generate post
# reviewed by human
# take feedback
# post to linkedin

#creating nodes constants
GENERATE_POST_NODE="GENERATE_POST_NODE"
# REVIEW_AND_TAKE_DECISION_NODE="REVIEW_AND_TAKE_DECISION_NODE"
FEEDBACK_NODE="FEEDBACK_NODE"
POST_NODE="POST_NODE"

class LinkedInPostCreaterState(TypedDict):
    messages: Annotated[list, add_messages]

llm = ChatGroq(model="llama-3.1-8b-instant")

def generate_post(state: LinkedInPostCreaterState):
    return {
        "messages": [llm.invoke(state["messages"])]
    }

def review_and_take_decision(state: LinkedInPostCreaterState):
    print("--------------This is the generated post---------------")
    print(state['messages'][-1].content)
    
    decision = input("Post to LinkedIn? yes/no\n")
    if decision.lower() == "yes":
        return POST_NODE
    else: 
        return FEEDBACK_NODE


def get_feedback(state: LinkedInPostCreaterState):
    feedback = input("How can we imporve the post?\n")
    return {
        "messages": [HumanMessage(content=feedback)]
    }



def publish_post(state: LinkedInPostCreaterState):
    print("------This is the Final Post-----")
    print(state["messages"][-1].content)




graph = StateGraph(LinkedInPostCreaterState)
graph.add_node(GENERATE_POST_NODE, generate_post)
# graph.add_node(REVIEW_AND_TAKE_DECISION_NODE, review_and_take_decision)
graph.add_node(FEEDBACK_NODE, get_feedback)
graph.add_node(POST_NODE,publish_post)

graph.set_entry_point(GENERATE_POST_NODE)



graph.add_conditional_edges(GENERATE_POST_NODE, review_and_take_decision)
graph.add_edge(FEEDBACK_NODE, GENERATE_POST_NODE)
graph.add_edge(POST_NODE, END)

app = graph.compile()

response = app.invoke({
    "messages": [HumanMessage(content="write a Linkedin post on AI taking over content creation")]
})
