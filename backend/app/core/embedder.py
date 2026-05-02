import httpx
from typing import List
from ..config import settings

class Embedder:
    def __init__(self):
        self.model_name = settings.EMBEDDING_MODEL
        self.base_url = f"{settings.OLLAMA_BASE_URL}/api/embeddings"

    def embed_text(self, text: str) -> List[float]:
        """Generate a vector for a single string using Ollama."""
        try:
            response = httpx.post(
                self.base_url,
                json={"model": self.model_name, "prompt": text},
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()["embedding"]
        except Exception as e:
            print(f"Ollama embedding failed: {e}")
            raise

    def embed_structure(self, structure_dict: dict) -> List[float]:
        """
        Convert the ExtractedStructure Pydantic object into a flat string
        and generate an embedding for it.
        """
        # We flatten the structure to capture its semantic essence for vector search
        flattened = f"{structure_dict.get('objective')} {structure_dict.get('problem_class')} " \
                    f"{structure_dict.get('equation_form')} {structure_dict.get('system_type')}"
        return self.embed_text(flattened)

# Singleton instance
embedder = Embedder()
