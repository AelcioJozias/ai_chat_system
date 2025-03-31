from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings  # Atualizado
from typing import List
import os


class KnowledgeBase:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2")  # Modelo atualizado
        self.vector_store = None

    def create_knowledge_base(self, documents: List[str], metadata: List[dict] = None):
        """Cria uma base de conhecimento a partir de documentos."""
        if metadata is None:
            metadata = [{} for _ in documents]

        if not documents:
            raise ValueError("No documents provided to create knowledge base")

        self.vector_store = FAISS.from_texts(documents, self.embeddings, metadatas=metadata)

    def save_knowledge_base(self, path: str):
        """Salva a base de conhecimento em disco."""
        if self.vector_store:
            self.vector_store.save_local(path)

    def load_knowledge_base(self, path: str):
        """Carrega uma base de conhecimento existente."""
        if os.path.exists(path):
            self.vector_store = FAISS.load_local(path, self.embeddings, allow_dangerous_deserialization=True)
        else:
            raise FileNotFoundError(f"No knowledge base found at {path}")

    def search_documents(self, query: str, k: int = 3) -> List[str]:
        """Busca documentos relevantes na base de conhecimento."""
        if not self.vector_store:
            raise ValueError("Knowledge base not initialized")

        docs = self.vector_store.similarity_search(query, k=k)
        return [doc.page_content for doc in docs]