import json
import os
import uuid
from typing import List
from sqlalchemy.orm import Session
from backend.app.db.session import SessionLocal
from backend.app.db.models import Method
from backend.app.core.embedder import embedder

def generate_method_summary(method_data: dict) -> str:
    """
    Create a semantic summary of the method that aligns with 
    how problem structures are embedded.
    """
    return f"{method_data.get('name')} {method_data.get('problem_class')} " \
           f"{method_data.get('equation_class')} {method_data.get('mathematical_core')}"

def seed_methods(db: Session, json_path: str):
    """
    Load methods from JSON, generate embeddings, and save to DB.
    """
    if not os.path.exists(json_path):
        print(f"Seed file not found: {json_path}")
        return

    with open(json_path, 'r') as f:
        methods_data = json.load(f)

    print(f"Found {len(methods_data)} methods to seed.")

    for data in methods_data:
        # Check if already exists
        existing = db.query(Method).filter(Method.name == data['name']).first()
        if existing:
            print(f"Skipping existing method: {data['name']}")
            continue

        # Generate embedding
        summary = generate_method_summary(data)
        embedding = embedder.embed_text(summary)

        # Create model instance
        method = Method(
            id=uuid.uuid4(),
            name=data['name'],
            aliases=data.get('aliases', []),
            origin_domain=data.get('origin_domain'),
            appears_in=data.get('appears_in', []),
            mathematical_core=data.get('mathematical_core'),
            problem_class=data.get('problem_class'),
            equation_class=data.get('equation_class'),
            constraint_type=data.get('constraint_type'),
            where_analogy_breaks=data.get('where_analogy_breaks', 'N/A'),
            assumptions=data.get('assumptions', []),
            runnable=data.get('runnable', False),
            python_implementation=data.get('python_implementation'),
            tags=data.get('tags', []),
            embedding=embedding,
            complexity_level=data.get('complexity_level'),
            typical_use_cases=data.get('typical_use_cases', []),
            known_limitations=data.get('known_limitations', [])
        )
        
        db.add(method)
        print(f"Added method: {data['name']}")

    db.commit()
    print("Seeding completed successfully.")

if __name__ == "__main__":
    # Get database session
    db = SessionLocal()
    try:
        # Resolve the JSON path relative to this script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_file = os.path.join(current_dir, "seed_data.json")
        seed_methods(db, json_file)
    finally:
        db.close()
