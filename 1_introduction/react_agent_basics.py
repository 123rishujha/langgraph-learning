from dotenv import load_dotenv
from langchain.agents import initialize_agent
from langchain_openai import ChatOpenAI
from langchain_community.tools import TavilySearchResults
import datetime

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo")

search_tool = TavilySearchResults(search_depth="basic")

def get_formatted_date_time(format: str = "%Y-%M-%D %H:%M:%S"):
    """ Returns current date and time in a specified format """
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime(format)
    return formatted_time


tools = [search_tool]


agent = initialize_agent(llm=llm, tools=tools, verbose=True, agent="zero-shot-react-description")

# agent.invoke("When was SpaceX's last launch")
agent.invoke("tomorrow's weather in delhi")


