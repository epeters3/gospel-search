import typing as t

from fastapi import FastAPI
from pydantic import BaseModel

from gospel_search.nlp_server.rerank import Reranker


reranker = Reranker()
app = FastAPI(title="HTTP NLP API Server")


class RerankRequest(BaseModel):
    query: str
    ranked_ids: t.List[str]


class RerankResult(BaseModel):
    result: t.List[dict]


@app.post("/api/rerank")
def rerank(body: RerankRequest):
    result = reranker.rerank(body.query, body.ranked_ids, 10)
    return RerankResult(result=result)
