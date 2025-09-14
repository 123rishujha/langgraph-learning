import json
from dotenv import load_dotenv
from typing import List, Dict, Any
from langchain_core.messages import AIMessage, BaseMessage, ToolMessage, HumanMessage
from langchain_community.tools import TavilySearchResults
from langchain_tavily import TavilySearch
from pprint import pprint

load_dotenv()

# tavily_tool = TavilySearchResults(max_results=5)
tavily_tool = TavilySearch(max_results=5)



def execute_tools(state: List[BaseMessage]) -> List[BaseMessage]:
    last_ai_message: AIMessage = state[-1]

    # if not hasattr(last_ai_message, "tools_calls") or not last_ai_message.tool_calls:
    # return []
    
    tool_messages = []
    
    for tool_call in last_ai_message.tool_calls:
        if tool_call["name"] in ["AnswerQuestion", "ReviseAnswer"]:
            call_id = tool_call["id"]
            search_queries = tool_call["args"].get("search_queries", [])

            query_results = {}
            for query in search_queries:
                result = tavily_tool.invoke(query)
                query_results[query] = result

            tool_messages.append(
                ToolMessage(
                    content=json.dumps(query_results),
                    tool_call_id=call_id
                )
            )

    return tool_messages


test_state = [
    HumanMessage(
        content="Write about how small business can leverage AI to grow"
    ),
    AIMessage(
        content="", 
        tool_calls=[
            {
                "name": "AnswerQuestion",
                "id": "call_KpYHichFFEmLitHFvFhKy1Ra",
                "args": {
                    'answer': '', 
                    'search_queries': [
                            'AI tools for small business', 
                            'AI in small business marketing', 
                            'AI automation for small business'
                    ], 
                    'reflection': {
                        'missing': '', 
                        'superfluous': ''
                    }
                },
            }
        ],
    )
]


# # Execute the tools
results = execute_tools(test_state)

# print(json.dumps([msg.dict() for msg in results], indent=2, ensure_ascii=False))

# print("Raw results:", results)
# if results:
    # parsed_content = json.loads(results[0].content)
    # print("Parsed content:", parsed_content)

