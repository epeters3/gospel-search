"""
Used to import all the segments from MongoDB into an
Chroma DB collection, for vector retrieval.
"""

from fire import Fire
from chromadb.utils.embedding_functions.sentence_transformer_embedding_function import SentenceTransformerEmbeddingFunction
from gospel_search.chroma.client import batch_stream, chroma, collection_exists
from gospel_search.utils import logger
from gospel_search.mongodb.segment import get_all_segments


SEGMENTS = "segments"


def import_docs(overwrite: bool = True, log_level: str = "INFO"):
    """
    Imports all segments from the Mongo DB into
    Chroma DB. If `overwrite == True`, the Chroma
    index will first be wiped out before indexing.
    """
    logger.setLevel(log_level)

    logger.info(f"importing '{SEGMENTS}' index from MongoDB to Vector DB...")

    if overwrite and collection_exists(chroma, SEGMENTS):
        logger.info("deleting all documents in the segments collection...")
        chroma.delete_collection(SEGMENTS)

    embed = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2", device="cuda")
    collection = chroma.get_or_create_collection(SEGMENTS, embedding_function=embed) # type: ignore

    batch_size = 256

    logger.info(f"indexing segments in batches of size {batch_size}...")
    for i, batch in enumerate(batch_stream(get_all_segments(), batch_size)):
        collection.add(
            ids=[d["_id"] for d in batch],
            metadatas=[{k: v for k, v in d.items() if k not in {"links"} and v is not None} for d in batch],
            documents=[d["text"] for d in batch],
        )
        logger.info(f"indexed batch {i + 1}")


if __name__ == "__main__":
    Fire(import_docs)
