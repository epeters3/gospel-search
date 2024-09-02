import os
from typing import Generator, Sequence, cast
from chromadb import EmbeddingFunction, HttpClient
from chromadb.utils.embedding_functions.sentence_transformer_embedding_function import SentenceTransformerEmbeddingFunction

from gospel_search.api.types import SearchResults


SEGMENTS = "segments"

class Chroma:
    def __init__(self):
        self.client = HttpClient(host=os.environ["CHROMA_HOST"], port=int(os.environ["CHROMA_PORT"]))
        self.embed = cast(EmbeddingFunction, SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2", device="cuda"))
        self.init_collection()
    
    def init_collection(self):
        self.collection = self.client.get_or_create_collection(SEGMENTS, embedding_function=self.embed)
    
    def delete_all(self):
        """Deletes all records in the collection."""
        self.client.delete_collection(SEGMENTS)
        self.init_collection()

    def collection_exists(self, name: str) -> bool:
        """Returns `True` if the given Chroma collection exists."""
        return name in {c.name for c in self.client.list_collections()}
    
    def search(self, query: str, k: int):
        res = self.collection.query(query_texts=[query], n_results=k)
        data = res["metadatas"]
        if not data:
            return SearchResults(results=[])
        return SearchResults(results=data[0])


def chunk[T](data: Sequence[T], n):
    """Yield successive n-sized chunks from `data`."""
    for i in range(0, len(data), n):
        yield data[i : i + n]

def batch_stream[T](stream: Generator[T, None, None], n):
    batch = []
    for item in stream:
        batch.append(item)
        if len(batch) == n:
            yield batch
            batch = []
    if batch:  # Yield the remaining items in the batch if any
        yield batch
