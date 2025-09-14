from dotenv import load_dotenv
load_dotenv()
from typing import TypedDict, Annotated, List
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, add_messages, START, END
from langgraph.types import interrupt, Command
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver
import uuid



llm = ChatGroq(model="llama-3.1-8b-instant")

class State(TypedDict):
    linkedin_topic: str
    generated_post: Annotated[List[str], add_messages]
    human_feedback: Annotated[List[str], add_messages]


def model(state: State):
    """Here we are using llm to generate linkedin post with human feedback incorporated"""

    linkedin_topic = state["linkedin_topic"]
    feedback = state["human_feedback"] if "human_feedback" in state else ["No feedback yet"]

    prompt = f"""

        LinkedIn Topic: {linkedin_topic}
        Human Feedback: {feedback[-1] if feedback else "No feedback yet"}

        Generate a structured and well-written LinkedIn post based on the given topic.

        Consider previous human feedback to refine the reponse. 
    """


    response = llm.invoke([
        SystemMessage(content="You are a linkedin post expert"),
        HumanMessage(content=prompt)
    ])

    generated_post = response.content
    print("\n------------generated post---------:\n", generated_post)

    return {
        "linkedin_topic": state["linkedin_topic"],
        "human_feedback": feedback,
        "generated_post": [AIMessage(content=generated_post)]
    }

def human_node(state: State):
    """Human Intervention node - loops back to model unless input is done"""
    print("\n [human_node] awaiting human feedback...")

    generated_post = state["generated_post"]

    user_feedback = interrupt({
        "generated_post": generated_post,
        "message":"provide feedback or type done to finish"
    })
    # user_feedback = interrupt("just testing.....")

    if user_feedback == "done":
        return Command(update={
            "human_feedback": ["finished"]
        }, goto="end_node")
    else:
        return Command(update={
            "human_feedback": [user_feedback] 
        }, goto="model")
    

def end_node(state: State): 
    """ Final node """
    print("\n[end_node] Process finished")
    print("Final Generated Post:", state["generated_post"][-1])
    print("Final Human Feedback", state["human_feedback"])
    return {"generated_post": state["generated_post"], "human_feedback": state["human_feedback"]}


graph = StateGraph(State)

graph.add_node("model",model)
graph.add_node("human_node",human_node)
graph.add_node("end_node", end_node)

graph.add_edge("model", "human_node")

graph.set_entry_point("model")
graph.set_finish_point("end_node")


checkpointer = MemorySaver()
app = graph.compile(checkpointer=checkpointer)

thread_config = {"configurable": {
    "thread_id": uuid.uuid4()
}}

linkedin_topic = input("Enter your LinkedIn topic: ")
initial_state = {
    "linkedin_topic": linkedin_topic, 
    "generated_post": [], 
    "human_feedback": []
}


for chunk in app.stream(initial_state, checkpointer=checkpointer, config=thread_config):
    for node_id, value in chunk.items():
        if node_id=="__interrupt__":
            while True:
                user_feedback = input("Provide feedback (or type 'done' when finished): ")

                app.invoke(Command(resume=user_feedback), config=thread_config)

                # Exit loop if user says done
                if user_feedback.lower() == "done":
                    break


