import argparse
import sys
import json
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.core.pipeline import Pipeline

def run_cli():
    parser = argparse.ArgumentParser(description="ISOMORPH Structural Analogy CLI")
    parser.add_argument("problem", type=str, help="Research problem in plain text")
    parser.add_argument("--json", action="store_true", help="Output raw JSON instead of formatted text")
    
    args = parser.parse_args()

    db = SessionLocal()
    try:
        pipeline = Pipeline(db)
        print(f"Analyzing structure for: {args.problem[:50]}...")
        
        response = pipeline.run(args.problem)
        
        if args.json:
            print(response.model_dump_json(indent=2))
        else:
            _print_formatted(response)
            
    finally:
        db.close()

def _print_formatted(response):
    if response.errors:
        print("\nERRORS DETECTED:")
        for err in response.errors:
            print(f"  - {err}")

    if not response.analogies:
        print("\nNo high-confidence structural analogies found.")
        return

    print(f"\nFOUND {len(response.analogies)} STRUCTURAL ANALOGIES (Confidence: {response.confidence:.2f}):")
    print("=" * 60)

    for i, analogy in enumerate(response.analogies, 1):
        print(f"\n{i}. METHOD: {analogy.method_name} ({analogy.similarity_score:.2f} similarity)")
        print(f"   DOMAIN OF ORIGIN: {analogy.origin_domain}")
        
        print("\n   STRUCTURAL MAPPING:")
        for var_p, var_m in analogy.mapping.variable_mapping.items():
            print(f"     - Variable: {var_p} -> {var_m}")
            
        print("\n   TRANSFERABLE ASPECTS:")
        for aspect in analogy.transferable_aspects:
            print(f"     - {aspect}")
            
        print("\n   FAILURE CONDITIONS (Where the analogy breaks):")
        for cond in analogy.failure_conditions:
            print(f"     - {cond}")
        
        if analogy.primitive:
            print(f"\n   RUNNABLE PRIMITIVE ATTACHED: {analogy.primitive.name}")
        
        print("-" * 60)

    print(f"\nTotal latency: {response.latency_ms}ms")

if __name__ == "__main__":
    run_cli()
