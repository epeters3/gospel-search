from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from gospel_search.api.types import AnswerResult
from gospel_search.chroma.client import Chroma
from gospel_search.utils import logger

app = FastAPI(name="Gospel Search API")
logger.info("Creating chroma client...")
chroma = Chroma()
logger.info("Client created.")

@app.get("/api/search")
def search(query: str, k: int = 10):
    return chroma.search(query, k)

@app.get("/api/qa")
def qa(query: str):
    # TODO: implement
    return AnswerResult(answer="this is your answer.")

# TODO: this only works when the user first visits the root page. It doesn't work when a user
# first visits one of the other pages.
app.mount("/", StaticFiles(directory="./gospel_search/ui/dist", html=True), name="ui")
