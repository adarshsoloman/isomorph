
import asyncio
import json
import os
import time
from datetime import datetime
from app.core.pipeline import Pipeline
from app.db.session import SessionLocal

async def run_evaluation():
    # Setup paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    test_cases_path = os.path.join(current_dir, "test_cases.json")
    
    # Create results filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_path = os.path.join(current_dir, f"evaluation_report_{timestamp}.txt")

    if not os.path.exists(test_cases_path):
        print(f"Error: {test_cases_path} not found.")
        return

    with open(test_cases_path, "r") as f:
        data = json.load(f)

    all_cases = data.get("golden_cases", []) + data.get("stress_cases", [])
    
    # Initialize DB and Pipeline
    db = SessionLocal()
    pipeline = Pipeline(db)
    
    try:
        with open(results_path, "w", encoding="utf-8") as report:
            report.write(f"ISOMORPH BACKEND EVALUATION REPORT\n")
            report.write(f"Timestamp: {timestamp}\n")
            report.write(f"Pipeline Version: v0.1\n")
            report.write("="*60 + "\n\n")

            for case in all_cases:
                case_id = case.get("id")
                name = case.get("name")
                desc = case.get("description")
                
                print(f"Evaluating {case_id}: {name}...")
                report.write(f"CASE {case_id}: {name}\n")
                report.write(f"INPUT: {desc}\n")
                report.write("-" * 40 + "\n")

                start_time = time.time()
                try:
                    # Run the actual pipeline
                    # Note: Pipeline.run is currently synchronous in pipeline.py
                    # If you change it to async later, this await is ready.
                    # For now, it might be a normal call. Checking pipeline.py...
                    # It's synchronous, so we'll call it normally.
                    result = pipeline.run(desc)
                    latency = (time.time() - start_time) * 1000

                    report.write(f"STATUS: SUCCESS\n")
                    report.write(f"LATENCY: {latency:.2f}ms\n")
                    # AnalysisResponse objects are used, not dicts
                    report.write(f"CONFIDENCE: {getattr(result, 'confidence', 0):.2f}\n")
                    
                    analogies = getattr(result, 'analogies', [])
                    report.write(f"FOUND: {len(analogies)} analogies\n\n")

                    for i, analogy in enumerate(analogies, 1):
                        report.write(f"  {i}. {getattr(analogy, 'method_name', 'N/A')} ({getattr(analogy, 'similarity_score', 0):.2f})\n")
                        report.write(f"     Origin: {getattr(analogy, 'origin_domain', 'N/A')}\n")
                        
                        mapping = getattr(analogy, 'mapping', {})
                        # Mapping is a pydantic model or dict
                        v_map = getattr(mapping, 'variable_mapping', {}) if hasattr(mapping, 'variable_mapping') else {}
                        report.write(f"     Variable Mapping: {v_map}\n")
                        
                        failures = getattr(analogy, 'failure_conditions', [])
                        report.write(f"     Failure Conditions: {', '.join(failures[:3])}...\n\n")

                    if getattr(result, 'errors', []):
                        report.write(f"ERRORS ENCOUNTERED: {result.errors}\n")

                except Exception as e:
                    report.write(f"STATUS: FAILED\n")
                    report.write(f"ERROR: {str(e)}\n")
                    import traceback
                    report.write(traceback.format_exc())
                
                report.write("\n" + "="*60 + "\n\n")
                print(f"Finished {case_id}.")

    finally:
        db.close()

    print(f"\nEvaluation complete! Report saved to: {results_path}")

if __name__ == "__main__":
    asyncio.run(run_evaluation())
