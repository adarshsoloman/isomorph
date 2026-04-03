import os
import sys
import uuid
import json
from typing import List, Dict, Any
from docx import Document
from sqlalchemy.orm import Session
from sqlalchemy import func

# Ensure we can import from backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))

from backend.app.db.session import SessionLocal
from backend.app.db.models import Method
from backend.app.core.embedder import embedder

def extract_methods_from_json(file_path: str) -> List[Dict[str, Any]]:
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r') as f:
        data = json.load(f)
    print(f"Loaded {len(data)} methods from {file_path}")
    return data

def extract_methods_from_docx(file_path: str) -> List[Dict[str, Any]]:
    if not os.path.exists(file_path):
        return []
    doc = Document(file_path)
    methods = []
    for table in doc.tables:
        rows = list(table.rows)
        header = [cell.text.strip().upper() for cell in rows[0].cells]
        start_row = 1 if "METHOD NAME" in header else 0
        for row_idx in range(start_row, len(rows)):
            cells = rows[row_idx].cells
            if len(cells) < 11: continue
            name = cells[0].text.strip()
            if not name or name == "METHOD NAME": continue
            methods.append({
                "name": name,
                "aliases": [a.strip() for a in cells[1].text.split(",") if a.strip()],
                "origin_domain": cells[2].text.strip(),
                "appears_in": [a.strip() for a in cells[3].text.split(",") if a.strip()],
                "mathematical_core": cells[4].text.strip(),
                "problem_class": cells[5].text.strip(),
                "equation_class": "unknown",
                "constraint_type": cells[6].text.strip(),
                "cross_domain_example_1": cells[7].text.strip(),
                "cross_domain_example_2": cells[8].text.strip(),
                "where_analogy_breaks": cells[9].text.strip(),
                "assumptions": [],
                "runnable": "yes" in cells[10].text.lower(),
                "python_implementation": cells[11].text.strip() if len(cells) > 11 else "N/A",
                "tags": [cells[5].text.strip().lower()],
                "complexity_level": "intermediate",
                "typical_use_cases": [cells[2].text.strip()],
                "known_limitations": [cells[9].text.strip()]
            })
    print(f"Extracted {len(methods)} methods from docx tables")
    return methods

def deep_seed(db: Session):
    base_path = os.path.dirname(__file__)
    data_dir = os.path.abspath(os.path.join(base_path, "../../../../data"))
    
    all_methods = []
    
    # 1. Load from Docx
    docx_file = os.path.join(data_dir, "Cross-Domain Scientific Method Knowledge Base.docx")
    all_methods.extend(extract_methods_from_docx(docx_file))
    
    # 2. Load from JSON batches
    batch_files = ["seed_data_batch_2.json", "seed_data_batch_3_refined.json"]
    for bf in batch_files:
        path = os.path.join(base_path, bf)
        data = extract_methods_from_json(path)
        # Normalize boolean fields
        for item in data:
            if isinstance(item.get("runnable"), str):
                item["runnable"] = item["runnable"].lower() == "yes"
        all_methods.extend(data)

    print(f"Total methods to process: {len(all_methods)}")

    loaded_count = 0
    for m_data in all_methods:
        try:
            # Normalization: ensure name is unique
            existing = db.query(Method).filter(Method.name == m_data['name']).first()
            if existing:
                continue

            # Text to embed
            text_to_embed = f"{m_data['name']}: {m_data['mathematical_core']}"
            embedding = embedder.embed_text(text_to_embed)

            method = Method(
                id=uuid.uuid4(),
                **m_data,
                embedding=embedding
            )
            db.add(method)
            loaded_count += 1
            if loaded_count % 20 == 0:
                print(f"Progress: {loaded_count} methods seeded...")
                db.commit()
        except Exception as e:
            db.rollback()
            print(f"Error seeding {m_data.get('name')}: {e}")

    db.commit()
    final_count = db.query(func.count(Method.id)).scalar()
    print(f"\nFinal Report:")
    print(f"- Unique Methods Seeded in this run: {loaded_count}")
    print(f"- Total Methods now in DB: {final_count}")

if __name__ == "__main__":
    db_session = SessionLocal()
    try:
        deep_seed(db_session)
    finally:
        db_session.close()
