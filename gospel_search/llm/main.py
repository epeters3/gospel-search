from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers.string import StrOutputParser

llm = ChatOpenAI(model='gpt-4o-2024-08-06')

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
        ("human", "{input}"),
    ]
)

qa_chain = prompt | llm | StrOutputParser
