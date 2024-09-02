from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from gospel_search.api.types import AnswerResult
from gospel_search.chroma.client import Chroma
from gospel_search.utils import logger
from gospel_search.llm.main import get_qa_chain

logger.info("Creating chroma client...")
chroma = Chroma()
logger.info("Client created.")
qa_chain = get_qa_chain(chroma)

api = FastAPI(name="Gospel Search API")

@api.get("/search")
def search(query: str, k: int = 10):
    return chroma.search(query, k)

@api.get("/qa")
def qa(query: str):
    answer = qa_chain.invoke({"query": query})
    return AnswerResult(answer=answer)

app = FastAPI(name="Gospel Search")

app.mount("/api", api)
# TODO: this only works when the user first visits the root page. It doesn't work when a user
# first visits one of the other pages. They have to explicitly specify .html for the other pages.
app.mount("/", StaticFiles(directory="./gospel_search/ui/dist", html=True), name="ui")
