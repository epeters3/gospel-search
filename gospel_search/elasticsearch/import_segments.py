"""
Used to import all the segments from MongoDB into an
ElasticSearch index, for retrieval.
"""
from collections import defaultdict
import typing as t

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
    MongoDB segments collection. Collects all
    segments for each conference talk or scripture
    chapter into a single document.
    """
    segments_collection = db[SEGMENTS]
    documents: t.Dict[str, dict] = defaultdict(
        lambda: {"_index": SEGMENTS, "segments": []}
    )

    logger.info("preprocessing segments into documents...")
    for segment in tqdm(segments_collection.find(), total=segments_collection.count()):
        # These fields will not go in the top-level document.
        segment.pop("_id")
        num = segment.pop("num")
        text = segment.pop("text")
        segment.pop("links")

        document = documents[segment["parent_id"]]
        document["segments"].append({"num": num, "text": text})
        for k, v in segment.items():
            # sanity check as we add this data to the document to make
            # sure we're not adding multiple segments to the same
            # document with differing document-level information.
            if k in document and document[k] != v:
                raise ValueError(
                    f"different value {v} found for the same key {k} in "
                    f"document {document} (original value {document[k]})"
                )
            document[k] = v

    logger.info("indexing documents...")
    for document in tqdm(documents.values()):
        # Rename the id field to the correct name (the ElasticSearch name),
        # since above we had to keep it what the segments call it.
        document["_id"] = document.pop("parent_id")
        # Sort the segments of each document to make sure they're in order.
        document["segments"].sort(key=lambda s: s["num"])
        yield document


def import_docs(overwrite: bool = True, log_level: str = "INFO"):
    """
    Imports all segments from the Mongo DB into
    ElasticSearch. If `overwrite == True`, the ES
    index will first be wiped out before indexing.
    """
    logger.setLevel(log_level)

    logger.info(f"importing '{SEGMENTS}' index from MongoDB to ElasticSearch...")

    if overwrite and es_client.indices.exists(SEGMENTS):
        logger.info("deleting all documents in the segments index...")
        es_client.indices.delete(SEGMENTS)

    bulk(es_client, get_docs_to_index())


if __name__ == "__main__":
    Fire(import_docs)
