from chromadb import Metadata
from pydantic import BaseModel


class SearchResults(BaseModel):
    # TODO: type the Segment type
    results: list[Metadata]

class AnswerResult(BaseModel):
    answer: str
