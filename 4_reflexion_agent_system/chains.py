from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain.schema import HumanMessage
from langchain_openai import ChatOpenAI
from schema import AnswerQuestion, ReviseAnswer
import datetime
# from pprint import pprint
# import json

load_dotenv()

actor_prompt_template = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are AI researcher
        Current Time: {time}
        1. {first_instruction}
        2. Reflect and critique your answer and be servere for maximum improvement
        3. After reflection **list 1-3 search queries separatly** for researching improvements. Do not include them inside reflection
        """
    ),
    MessagesPlaceholder(variable_name="messages"),
    ("system","Anser the users questions above using the required format.")
]).partial(
    time=lambda: datetime.datetime.now().isoformat(),
)

first_responder_prompt_template = actor_prompt_template.partial(
    first_instruction="Provide a detailed 250 word answer"
)

llm = ChatOpenAI(model="gpt-3.5-turbo")

first_responder_chain = first_responder_prompt_template | llm.bind_tools(tools=[AnswerQuestion], tool_choice="AnswerQuestion")

revise_instructions = """Revise your previous answer using the new information.
    - You should use the previous critique to add important information to your answer.
        - You MUST include numerical citations in your revised answer to ensure it can be verified.
        - Add a "References" section to the bottom of your answer (which does not count towards the word limit). In form of:
            - [1] https://example.com
            - [2] https://example.com
    - You should use the previous critique to remove superfluous information from your answer and make SURE it is not more than 250 words.
"""

revisor_chain = actor_prompt_template.partial(first_instruction=revise_instructions) | llm.bind_tools(tools=[ReviseAnswer], tool_choice="ReviseAnswer")


# response = first_responder_chain.invoke({
#     "messages": [HumanMessage(content="AI agents taking over content creation.")]
# })
# print(response)
# print("---------------------------------- ########################################## ----------------------------------")

# print(json.dumps(response.dict(), indent=2, ensure_ascii=False))

