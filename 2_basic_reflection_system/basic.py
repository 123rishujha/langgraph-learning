from dotenv import load_dotenv
from langgraph.graph import MessageGraph, END
from chains import generation_chain,reflection_chain
from langchain_core.messages import HumanMessage


GENERATE='generate'
REFLECT='reflect'
graph = MessageGraph()

def generate_node(state):
    return generation_chain.invoke({"messages": state})

def reflect_node(state):
    respnonse = reflection_chain.invoke({"messages": state})
    return [HumanMessage(content=respnonse.content)]



graph.add_node(GENERATE, generate_node)
graph.add_node(REFLECT, reflect_node)
graph.set_entry_point(GENERATE)

def should_continue(state):
    if (len(state) > 6):
        return END
    return REFLECT


graph.add_conditional_edges(
    GENERATE, 
    should_continue,
    {
        REFLECT: REFLECT, 
        END: END
    }
)

graph.add_edge(REFLECT, GENERATE)


app = graph.compile()

print(app.get_graph().draw_mermaid())
app.get_graph().print_ascii()

# response = app.invoke(HumanMessage(content="AI agent taking over content creation"))
# print(response)
