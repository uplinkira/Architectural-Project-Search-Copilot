from langchain_core.embeddings import Embeddings
from sentence_transformers import SentenceTransformer


class M3eEmbeddings(Embeddings):
    model = SentenceTransformer("moka-ai/m3e-base")

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        embeddings = self.model.encode(texts).tolist()
        return embeddings

    def embed_query(self, text: str) -> list[float]:
        embeddings = self.model.encode(text).tolist()
        return embeddings
