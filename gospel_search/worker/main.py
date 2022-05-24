from fastapi import FastAPI
from gospel_search.elasticsearch.import_segments import import_docs
from gospel_search.mongodb.compute_embeddings import compute_embeddings
from gospel_search.mongodb.extract_segments import extract_segments

from gospel_search.mongodb.pull_pages import pull_pages
from gospel_search.worker.schemas import (
    ComputeEmbeddingsConfig,
    ExtractSegmentsConfig,
    ImportDocsConfig,
    PullPagesConfig,
)


app = FastAPI(
    description="Worker server with endpoints to execute the ETL tasks used throughout the system's entire data pipeline."
)


@app.put("/crawl")
def crawl(cfg: PullPagesConfig):
    """
    Crawls the online gospel library to extract all the raw html pages of the scriptures and conference talks,
    saving them all in the `pages` collection of the `gospel_search` database in MongoDB.
    """
    pull_pages(**cfg.dict())


@app.put("/extract")
def extract(cfg: ExtractSegmentsConfig):
    """
    Extracts segments (paragraphs or verses) from all the content previously
    crawled by the `crawl` step. Saves the results to the `segments` table in
    the `gospel_search` database.
    """
    extract_segments(**cfg.dict())


@app.put("/embed")
def embed(cfg: ComputeEmbeddingsConfig):
    """
    Computes and saves sentence embeddings for all the segments in the
    `segments` MongoDB table that don't already have embeddings.
    """
    compute_embeddings(**cfg.dict())


@app.put("/populate-es")
def populate_es(cfg: ImportDocsConfig):
    """Loads all the segments from MongoDB into the ElasticSearch instance."""
    import_docs(**cfg.dict())
