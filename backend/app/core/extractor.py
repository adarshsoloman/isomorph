import json
from groq import Groq
from ..config import settings
from ..schemas.extraction import ExtractedStructure

class Extractor:
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = "llama-3.3-70b-versatile"

    def extract(self, input_text: str) -> ExtractedStructure:
        """
        Extract structured data from raw research text using Groq.
        Retries once on invalid JSON/validation failure.
        """
        schema_info = (
            "JSON SCHEMA:\n"
            "{\n"
            "  \"objective\": \"string\",\n"
            "  \"variables\": [\"string\"],\n"
            "  \"constraints\": [\"string\"],\n"
            "  \"system_type\": \"deterministic\" | \"stochastic\" | \"hybrid\",\n"
            "  \"equation_form\": \"string\",\n"
            "  \"optimization_type\": \"min\" | \"max\" | \"equilibrium\" | \"unknown\",\n"
            "  \"problem_class\": \"differential equation\" | \"optimization\" | \"inference\" | \"simulation\",\n"
            "  \"domain_hint\": \"string (optional)\"\n"
            "}"
        )

        system_prompt = (
            "You are a structural analyst for scientific problems. "
            "Your goal is to extract the underlying mathematical and system structure "
            "from a researcher's problem description.\n\n"
            f"{schema_info}\n\n"
            "CRITICAL: Use ONLY the allowed values for literal fields. Return ONLY valid JSON."
        )
        
        user_prompt = f"Problem description: {input_text}\n\nReturn structure JSON:"

        try:
            return self._call_groq(system_prompt, user_prompt)
        except Exception as e:
            # Simple retry logic as per PRD
            print(f"Extraction attempt 1 failed: {e}. Retrying with stricter instructions.")
            stricter_user_prompt = (
                f"{user_prompt}\n\n"
                "CRITICAL: Ensure the response is exactly JSON. No markdown, no preamble."
            )
            return self._call_groq(system_prompt, stricter_user_prompt)

    def _call_groq(self, system_prompt: str, user_prompt: str) -> ExtractedStructure:
        chat_completion = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            model=self.model,
            response_format={"type": "json_object"}
        )
        
        response_json = json.loads(chat_completion.choices[0].message.content)
        return ExtractedStructure(**response_json)

# Singleton instance
extractor = Extractor()
