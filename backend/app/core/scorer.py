import json
from typing import List, Optional
from groq import Groq
from ..config import settings
from ..schemas.extraction import ExtractedStructure
from ..schemas.analogy import ScoredAnalogy, AnalogyMapping
from ..db.models import Method

class Scorer:
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = "llama-3.3-70b-versatile"

    def score_analogy(
        self, 
        input_text: str, 
        extracted_structure: ExtractedStructure, 
        candidate_method: Method
    ) -> Optional[ScoredAnalogy]:
        """
        Compare a research problem to a candidate method using Groq.
        Produces a similarity score, mapping, and failure conditions.
        """
        system_prompt = (
            "You are a scientific analogy expert. Compare the research problem to "
            "the mathematical method provided. Focus on structural isomorphism, not jargon."
            "Return ONLY valid JSON matching the ScoredAnalogy schema."
        )

        user_prompt = (
            f"RESEARCH PROBLEM:\n{input_text}\n\n"
            f"EXTRACTED STRUCTURE:\n{extracted_structure.model_dump_json()}\n\n"
            f"CANDIDATE METHOD:\nName: {candidate_method.name}\n"
            f"Mathematical Core: {candidate_method.mathematical_core}\n"
            f"Origin Domain: {candidate_method.origin_domain}\n\n"
            "Return ScoredAnalogy JSON:"
        )

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                model=self.model,
                response_format={"type": "json_object"}
            )
            
            response_json = json.loads(chat_completion.choices[0].message.content)
            
            # Enrich with database data
            response_json["method_name"] = candidate_method.name
            response_json["origin_domain"] = candidate_method.origin_domain
            response_json["appears_in"] = candidate_method.appears_in
            
            # The LLM generates: similarity_score, mapping, transferable_aspects, 
            # non_transferable_aspects, failure_conditions
            
            return ScoredAnalogy(**response_json)
        except Exception as e:
            print(f"Scoring failed for {candidate_method.name}: {e}")
            return None

# Singleton instance
scorer = Scorer()
