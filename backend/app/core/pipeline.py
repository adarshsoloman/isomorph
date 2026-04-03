import time
from typing import List
from sqlalchemy.orm import Session

from .extractor import extractor
from .embedder import embedder
from .matcher import matcher
from .scorer import scorer
from .primitive_fetcher import primitive_fetcher
from ..schemas.analogy import AnalysisResponse, ScoredAnalogy
from ..config import settings

class Pipeline:
    def __init__(self, db: Session):
        self.db = db

    def run(self, input_text: str) -> AnalysisResponse:
        """
        Orchestrate the 6-step ISOMORPH pipeline.
        """
        start_time = time.time()
        response = AnalysisResponse(input_text=input_text)
        
        # 1. EXTRACTOR
        try:
            extracted_structure = extractor.extract(input_text)
            response.extracted_structure = extracted_structure
        except Exception as e:
            response.errors.append(f"extractor_failed: {str(e)}")
            return self._finalize(response, start_time)

        # 2. EMBEDDER
        try:
            embedding = embedder.embed_structure(extracted_structure.model_dump())
        except Exception as e:
            response.errors.append(f"embedder_failed: {str(e)}")
            return self._finalize(response, start_time)

        # 3. MATCHER
        try:
            matches = matcher.find_top_k(self.db, embedding)
        except Exception as e:
            response.errors.append(f"matcher_failed: {str(e)}")
            return self._finalize(response, start_time)

        # 4. SCORER (Step 4 & 5 Validator)
        scored_analogies = []
        for method in matches:
            analogy = scorer.score_analogy(input_text, extracted_structure, method)
            if analogy and analogy.similarity_score >= settings.MIN_SIMILARITY_SCORE:
                # 6. PRIMITIVE FETCHER
                analogy.primitive = primitive_fetcher.fetch_for_method(method.name)
                scored_analogies.append(analogy)

        response.analogies = scored_analogies
        
        # Calculate overall confidence (mean similarity score)
        if scored_analogies:
            response.confidence = sum(a.similarity_score for a in scored_analogies) / len(scored_analogies)

        return self._finalize(response, start_time)

    def _finalize(self, response: AnalysisResponse, start_time: float) -> AnalysisResponse:
        response.latency_ms = int((time.time() - start_time) * 1000)
        return response

# Note: We create Pipeline instances within the request lifecycle 
# because it requires a DB session.
