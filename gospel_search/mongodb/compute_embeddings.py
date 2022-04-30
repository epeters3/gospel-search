from fire import Fire
from tqdm import tqdm

from gospel_search.mongodb.client import db
from gospel_search.nlp_server.text_embedder import TextEmbedder
from gospel_search.utils import logger


def compute_embeddings(overwrite: bool = False):
    """
    Computes all the embeddings for all the segments in the database
    """
    segments_collection = db.segments
    embedder = TextEmbedder()

    logger.info("computing an embedding vector for each segment...")
    # load them all into memory at once so our MongoDB connection doesn't
    # drop part way through.
    segments = list(segments_collection.find())
    for segment in tqdm(segments):
        if not overwrite and "embedding" in segment:
            # This segment already has an embedding and we're not replacing it.
            continue
        embedding = embedder.embed_text(segment["text"])
        segments_collection.find_one_and_update(
            # The list is stored in the database as a raw list, not a numpy array.
            {"_id": segment["_id"]},
            {"$set": {"embedding": embedding.tolist()}},
        )
    logger.info("embedding complete")


if __name__ == "__main__":
    Fire(compute_embeddings)
