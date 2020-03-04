from sentence_transformers import SentenceTransformer
from nltk.tokenize import sent_tokenize
import numpy as np
from scipy.spatial.distance import cosine


class TextEmbedder:
    def __init__(self):
        self.sentence_embedder = SentenceTransformer(
            "distilbert-base-nli-stsb-mean-tokens"
        )

    def similarity(self, a: np.ndarray, b: np.ndarray):
        """
        Computes the cosine similarity between vectors `a` and `b`.
        """
        return -(cosine(a, b) - 1)

    def embed_text(self, text: str) -> np.ndarray:
        """
        Embeds `text`, where text can be one or more sentences. An
        embedding vector is created for every sentence, and the result
        is computed as the average of those vectors. This is because
        the quality of sentence embeddings tends to deteriorate as the
        length of the "sentence" increases.
        """
        sentences = sent_tokenize(text)
        sent_vecs = self.sentence_embedder.encode(sentences)
        return np.mean(sent_vecs, axis=0)
