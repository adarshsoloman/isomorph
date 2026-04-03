import json
import os
from groq import Groq
from pydantic import BaseModel, Field
from typing import List

# Setup Groq Client
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in environment variables")
client = Groq(api_key=GROQ_API_KEY)

class RefinedFields(BaseModel):
    problem_class: str
    equation_class: str
    constraint_type: str
    tags: List[str]

def refine_method(method: dict) -> dict:
    """Use Groq to fill missing fields for a single method."""
    
    # Only refine if fields are missing
    if method.get("problem_class") and method.get("equation_class"):
        return method

    prompt = (
        f"Method Name: {method['name']}\n"
        f"Mathematical Core: {method['mathematical_core']}\n"
        f"Origin Domain: {method['origin_domain']}\n\n"
        "Fill the following missing fields for this scientific method. "
        "Use ONLY the specific categories below for problem_class.\n"
        "problem_class must be one of: 'differential equation', 'optimization', 'inference', 'simulation'.\n"
        "Return ONLY valid JSON matching this schema:\n"
        "{\n"
        "  \"problem_class\": \"string\",\n"
        "  \"equation_class\": \"string\",\n"
        "  \"constraint_type\": \"string\",\n"
        "  \"tags\": [\"string\"]\n"
        "}"
    )

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a scientific structural analyst. Return ONLY JSON."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"}
        )
        
        refined_data = json.loads(chat_completion.choices[0].message.content)
        
        # Update original method
        method["problem_class"] = refined_data.get("problem_class", "simulation")
        method["equation_class"] = refined_data.get("equation_class", "unknown")
        method["constraint_type"] = refined_data.get("constraint_type", "none")
        method["tags"] = refined_data.get("tags", [])
        
        print(f"Refined: {method['name']}")
        return method

    except Exception as e:
        print(f"Error refining {method['name']}: {e}")
        # Sensible defaults
        method["problem_class"] = method.get("problem_class") or "simulation"
        method["equation_class"] = method.get("equation_class") or "unknown"
        method["constraint_type"] = method.get("constraint_type") or "none"
        method["tags"] = method.get("tags") or ["scientific-computing"]
        return method

def process_batch():
    base_path = "backend/app/db/seed"
    input_file = os.path.join(base_path, "seed_data_batch_3.json")
    output_file = os.path.join(base_path, "seed_data_batch_3_refined.json")

    if not os.path.exists(input_file):
        print(f"File not found: {input_file}")
        return

    with open(input_file, 'r') as f:
        methods = json.load(f)

    print(f"Starting refinement of {len(methods)} methods...")
    
    refined_methods = []
    for m in methods:
        refined_methods.append(refine_method(m))

    with open(output_file, 'w') as f:
        json.dump(refined_methods, f, indent=4)

    print(f"Successfully saved refined data to {output_file}")

if __name__ == "__main__":
    process_batch()
