"""
Used to import all the segments from MongoDB into an
ElasticSearch index, for retrieval.
"""
from tqdm import tqdm
from elasticsearch.helpers import bulk
from fire import Fire

from gospel_search.elasticsearch.client import client as es_client
from gospel_search.mongodb.client import db
from gospel_search.utils import logger


SEGMENTS = "segments"


def get_docs_to_index():
    """
    Generates elastic search documents from the
    MongoDB segments collection.
    """
    segments_collection = db[SEGMENTS]
    for segment in tqdm(segments_collection.find(), total=segments_collection.count()):
        _id = segment.pop("_id")
        yield {
            "_index": SEGMENTS,
            "_id": _id,
            "_source": segment,
        }


def import_docs(refresh: bool = True, log_level: str = "INFO"):
    """
    Imports all segments from the Mongo DB into
    ElasticSearch. If `refresh == True`, the ES
    index will first be wiped out before indexing.
    """
    logger.setLevel(log_level)

    logger.info(f"importing '{SEGMENTS}' index from MongoDB to ElasticSearch...")

    if refresh and es_client.indices.exists(SEGMENTS):
        logger.info("deleting all documents in the segments index...")
        es_client.indices.delete(SEGMENTS)

    bulk(es_client, get_docs_to_index())


if __name__ == "__main__":
    Fire(import_docs)
