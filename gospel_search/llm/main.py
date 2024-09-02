from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers.string import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables import chain

from gospel_search.api.types import SearchResult
from gospel_search.chroma.client import Chroma
    

def stringify_search_result(result: SearchResult) -> str:
    segment = result.segment
    return f"""Reference name: {segment.name}
Text: ${segment.text}
Link: ${segment.parent_id}
"""

llm = ChatOpenAI(model='gpt-4o-2024-08-06')

def Retriever(*, k: int, chroma: Chroma):
    @chain
    def retrieve(input):
        res = chroma.search(input["query"], k)
        return "\n".join([stringify_search_result(r) for r in res.results])
    
    return retrieve


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a helpful assistant assisting with answering questions
related to the gospel of the Church of Jesus Christ of Latter-day Saints.
Only answer gospel and doctrine-related questions. Here are some retrieved
scripture verses and general conference talk paragraphs related to the user's
query. Use them to answer the user's question.

Related scripture verses and conference talk paragraphs:

{results}
""",
        ),
        ("human", "{query}"),
    ]
)

def get_qa_chain(chroma: Chroma):
    return {"query": RunnablePassthrough(), "results": Retriever(k=25, chroma=chroma)} | prompt | llm | StrOutputParser()
