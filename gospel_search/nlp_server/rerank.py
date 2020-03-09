import typing as t

from scipy.spatial.distance import cosine
from tqdm import tqdm

from gospel_search.mongodb.segment import get_segments_by_document
from gospel_search.utils import logger
from gospel_search.nlp_server.text_embedder import TextEmbedder


class Reranker:
    """
    Reranks search results, given a query and a list of
    Elastic Search's top returned document ids. Reranks
    at the segment (i.e. paragraph) level of the documents
    using natural language processing.
    """

    def __init__(self):
        self.documents = get_segments_by_document(include_embeddings=True)
        self.embedder = TextEmbedder()

    def rerank(self, query: str, ranked_ids: t.List[str], n: int) -> t.List[dict]:
        """
        Parameters
        ----------
        query:
            The user's query they are searching for results with.
        ranked_ids:
            The ordered list of ids representing the documents
            Elastic Search identified as the top hits for the
            user's query.
        n:
            The number of search results desired.
        """
        query_embedding = self.embedder.embed_text(query)
        # Score the query with every segment embedding in the original
        # ranked documents, returning the segments sorted by score, but
        # not the embedding vectors, because those are large and not needed.
        ranked_segments = []
        for doc_id in ranked_ids:
            doc = self.documents[doc_id]
            for segment in doc["segments"]:
                score = self.embedder.similarity(query_embedding, segment["embedding"])
                ranked_segments.append(
                    {
                        # Don't return the embedding to the user; it's really big and
                        # they don't need it.
                        **{k: v for k, v in segment.items() if k != "embedding"},
                        "score": score,
                    }
                )

        ranked_segments.sort(key=lambda s: s["score"], reverse=True)
        return ranked_segments[:n]
