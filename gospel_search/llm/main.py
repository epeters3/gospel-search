from operator import itemgetter
import re
from typing import NotRequired, TypedDict
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers.string import StrOutputParser
from langchain_core.runnables import (
    Runnable,
    chain,
    RunnableParallel,
)

from gospel_search.api.types import AnswerResult, SearchResult
from gospel_search.chroma.client import Chroma




class ChainState(TypedDict):
    query: str
    results: NotRequired[list[SearchResult]]
    results_ctx: NotRequired[str]
    answer: NotRequired[str]


def stringify_search_result(result: SearchResult) -> str:
    segment = result.segment
    return f"""ID: {segment.id}
Name: {segment.name}
Text: {segment.text}
"""


llm = ChatOpenAI(model="gpt-4o-2024-08-06")


def Retriever(*, k: int, chroma: Chroma):
    @chain
    def retrieve(input: ChainState):
        res = chroma.search(input["query"], k)
        return [r for r in res.results]

    return retrieve


@chain
def stringify_results(state: ChainState):
    if "results" not in state:
        raise ValueError("results required")
    res = "\n".join([stringify_search_result(r) for r in state["results"]])
    print("RESULTS CONTEXT:")
    print(res)
    return res


@chain
def compose_answer(state: ChainState):
    if "answer" not in state or "results" not in state:
        raise ValueError("answer and results required")
    answer = state["answer"]
    id_matches: list[str] = re.findall(r"\[.+?\]", answer)
    ids = {id[1:-1] for id in id_matches}  # remove the brackets
    references = [r for r in state["results"] if r.segment.id in ids]
    return AnswerResult(answer=answer, references=references)


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a helpful assistant assisting with answering questions
related to the gospel of the Church of Jesus Christ of Latter-day Saints. Your
purpose is to help others build faith in Christ and connect with the holy
scriptures and the words of God's living prophets. Only answer gospel and
doctrine-related questions. Below will be some retrieved scripture verses and
general conference talk paragraphs related to the user's query. Use them
to answer the user's question.

Always cite your sources using inline citations. Every reference has an an ID. 
Cite your sources inline using square brackets around the source's full ID like
so: `[ID]`.

Related scripture verses and conference talk paragraphs:

{results_ctx}
""",
        ),
        ("human", "{query}"),
    ]
)


def get_qa_chain(chroma: Chroma) -> Runnable[ChainState, AnswerResult]:
    return (
        RunnableParallel(
            {"query": itemgetter("query"), "results": Retriever(k=25, chroma=chroma)}
        )
        | RunnableParallel(
            {
                "query": itemgetter("query"),
                "results": itemgetter("results"),
                "results_ctx": stringify_results,
            }
        )
        | RunnableParallel({"answer": prompt | llm | StrOutputParser(), "results": itemgetter("results")})
        | compose_answer
    )
