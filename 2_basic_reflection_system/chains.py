from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import MessagesPlaceholder,ChatPromptTemplate
load_dotenv()

generate_prompt = ChatPromptTemplate.from_messages([
     (
        "system",
        "You are a twitter techie influencer assistant tasked with writing excellent twitter posts."
        " Generate the best twitter post possible for the user's request."
        " If the user provides critique, respond with a revised version of your previous attempts.",
    ),
    MessagesPlaceholder(variable_name="messages")
])


reflection_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a viral twitter influencer grading a tweet. Generate critique and recommendations for the user's tweet."
        "Always provide detailed recommendations, including requests for length, virality, style, etc.",
    ),
    MessagesPlaceholder(variable_name="messages")  
])


llm = ChatOpenAI(model="gpt-3.5-turbo")

generation_chain = generate_prompt | llm
reflection_chain = reflection_prompt | llm
