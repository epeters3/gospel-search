import os
from typing import Generator, Sequence
from chromadb import HttpClient
from chromadb.api import ClientAPI

chroma = HttpClient(host=os.environ["CHROMA_HOST"], port=int(os.environ["CHROMA_PORT"]))


def collection_exists(client: ClientAPI, name: str) -> bool:
    """Returns `True` if the given Chroma collection exists."""
    return name in {c.name for c in client.list_collections()}


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
