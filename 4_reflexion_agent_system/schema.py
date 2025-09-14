from pydantic import BaseModel, Field
from typing import List

class Reflection(BaseModel):
    missing: str = Field(description="Critique of what is missing.")
    superfluous: str = Field(description="Critique of what is superfluous")


class AnswerQuestion(BaseModel):
    "Answer the question"
    answer: str = Field(description="~250 words detailed answer of question")
    reflection: Reflection = Field(description="your reflection on initial answer")
    search_queries: List[str] = Field(description="1-3 search queries to research and improve your initial response")


class ReviseAnswer(AnswerQuestion):
    "Revise yours original answer to your question."
    references: List[str] = Field(description="Citations motivating your revised answer.")

