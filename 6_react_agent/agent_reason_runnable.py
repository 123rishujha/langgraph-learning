from dotenv import load_dotenv
from langchain.agents import create_react_agent, tool
from langchain_openai import ChatOpenAI
from langchain import hub
import datetime
from langchain_community.tools import TavilySearchResults


load_dotenv()


llm = ChatOpenAI(model="gpt-3.5-turbo")

search_tool = TavilySearchResults(search_depth="basic")

@tool
def get_formatted_date_time(format: str = "%Y-%M-%D %H:%M:%S"):
    """Return current date time in specified format"""
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime(format)
    return formatted_time


tools = [search_tool, get_formatted_date_time]

react_prompt = hub.pull("hwchase17/react")

react_agent_runnable = create_react_agent(llm=llm, tools=tools, prompt=react_prompt)

