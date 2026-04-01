from typing import List
from sqlalchemy.orm import Session
from ..db.models import Method
from ..schemas.extraction import ExtractedStructure

class Matcher:
    def find_top_k(self, db: Session, query_embedding: List[float], k: int = 5) -> List[Method]:
        """
        Find top k structurally analogous methods using pgvector cosine similarity.
        """
        # We use pgvector's cosine distance operator (<=>)
        # Cosine distance = 1 - Cosine similarity
        # We sort by distance ascending (meaning similarity descending)
        
        matches = db.query(Method).order_by(
            Method.embedding.cosine_distance(query_embedding)
        ).limit(k).all()
        
        return matches

# Singleton instance
matcher = Matcher()
