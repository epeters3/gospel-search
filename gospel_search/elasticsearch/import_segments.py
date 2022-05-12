"""
Used to import all the segments from MongoDB into an
ElasticSearch index, for retrieval.
"""
from elasticsearch.helpers import bulk
from fire import Fire
from tqdm import tqdm

from gospel_search.elasticsearch.client import client as es_client
from gospel_search.utils import logger
from gospel_search.mongodb.segment import get_segments_by_document


SEGMENTS = "segments"


def import_docs(overwrite: bool = True, log_level: str = "INFO"):
    """
    Imports all segments from the Mongo DB into
    ElasticSearch. If `overwrite == True`, the ES
    index will first be wiped out before indexing.
    """
    logger.setLevel(log_level)

    logger.info(f"importing '{SEGMENTS}' index from MongoDB to ElasticSearch...")

    if overwrite and es_client.indices.exists(index=SEGMENTS):
        logger.info("deleting all documents in the segments index...")
        es_client.indices.delete(index=SEGMENTS)

    documents = get_segments_by_document()
    for doc in documents.values():
        # Add the index name for Elastic Search.
        doc["_index"] = SEGMENTS

    logger.info("indexing documents...")
    bulk(es_client, tqdm(documents.values()))


if __name__ == "__main__":
    Fire(import_docs)
