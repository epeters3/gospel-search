from typing import Literal
from pydantic import BaseModel, Field

class BaseSegment(BaseModel):
  id: str
  parent_id: str
  num: int
  text: str
  name: str

class TalkSegment(BaseSegment):
  doc_type: Literal["general-conference"]
  talk_id: str
  month: int
  year: int

class VerseSegment(BaseSegment):
  doc_type: Literal["scriptures"]

class SearchResult(BaseModel):
   segment: TalkSegment | VerseSegment = Field(..., discriminator="doc_type")

class SearchResults(BaseModel):
    results: list[SearchResult]


class AnswerResult(BaseModel):
    answer: str
