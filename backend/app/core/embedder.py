from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List

class Embedder:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed_text(self, text: str) -> List[float]:
        """Generate a vector for a single string."""
        embedding = self.model.encode(text)
        return embedding.tolist()

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
