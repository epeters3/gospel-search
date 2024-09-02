"""
Used to import all the segments from MongoDB into an
Chroma DB collection, for vector retrieval.
"""

from fire import Fire
from chromadb.utils.embedding_functions.sentence_transformer_embedding_function import SentenceTransformerEmbeddingFunction
from gospel_search.chroma.client import SEGMENTS, Chroma, batch_stream
from gospel_search.utils import logger
from gospel_search.mongodb.segment import get_all_segments


def import_docs(overwrite: bool = True, log_level: str = "INFO"):
    """
    Imports all segments from the Mongo DB into
    Chroma DB. If `overwrite == True`, the Chroma
    index will first be wiped out before indexing.
    """
    chroma = Chroma()
    logger.setLevel(log_level)

    logger.info(f"importing '{SEGMENTS}' index from MongoDB to Vector DB...")

    if overwrite:
        logger.info("deleting all documents in the segments collection...")
        chroma.delete_all()

    batch_size = 256
    logger.info(f"indexing segments in batches of size {batch_size}...")
    for i, batch in enumerate(batch_stream(get_all_segments(), batch_size)):
        chroma.collection.add(
            ids=[d["_id"] for d in batch],
            metadatas=[{k: v for k, v in d.items() if k not in {"links"} and v is not None} for d in batch],
            documents=[d["text"] for d in batch],
        )
        logger.info(f"indexed batch {i + 1}")


if __name__ == "__main__":
    Fire(import_docs)
