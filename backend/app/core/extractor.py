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
            "  \"is_scientific\": boolean,\n"
            "  \"structure_confidence\": float (0.0 to 1.0),\n"
            "  \"rejection_reason\": \"string (only if is_scientific is false)\",\n"
            "  \"objective\": \"string\",\n"
            "  \"variable_roles\": {\n"
            "    \"state\": [\"string\"],\n"
            "    \"control\": [\"string\"],\n"
            "    \"noise\": [\"string\"],\n"
            "    \"parameters\": [\"string\"]\n"
            "  },\n"
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
            "CRITICAL RULES:\n"
            "1. GATEKEEPER: If the input is nonsense, purely poetic, or does not describe a "
            "scientific/engineering problem, set is_scientific to false and provide a rejection_reason.\n"
            "2. VARIABLE ROLES:\n"
            "   - state: internal variables that define the system's condition.\n"
            "   - control: variables the user can change to influence the outcome.\n"
            "   - noise: unpredictable elements or stochastic variables.\n"
            "   - parameters: constant values that define the system's behavior.\n"
            "3. LITERALS:\n"
            "   - system_type MUST be one of: [deterministic, stochastic, hybrid]\n"
            "   - optimization_type MUST be one of: [min, max, equilibrium, unknown]\n"
            "   - problem_class MUST be one of: [differential equation, optimization, inference, simulation]\n"
            "4. Return ONLY valid JSON."
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
            response_format={"type": "json_object"},
            temperature=0
        )
        
        response_json = json.loads(chat_completion.choices[0].message.content)
        # Handle cases where optional fields might be missing if LLM fails to include them
        if "variable_roles" not in response_json:
            response_json["variable_roles"] = {"state": [], "control": [], "noise": [], "parameters": []}
            
        return ExtractedStructure(**response_json)

# Singleton instance
extractor = Extractor()
