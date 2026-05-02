
import json
import os
import uuid
from sqlalchemy.orm import Session
from sqlalchemy import text as sa_text
from app.db.session import SessionLocal
from app.db.models import Method, Primitive
from app.core.embedder import embedder
from app.primitives.registry import PRIMITIVE_REGISTRY, get_primitive_for_method

def generate_method_summary(method_data: dict) -> str:
    return f"{method_data.get('name')} {method_data.get('problem_class')} " \
           f"{method_data.get('equation_class')} {method_data.get('mathematical_core')}"

def seed_database():
    db = SessionLocal()
    try:
        # 0. Clean the database
        print("Truncating tables...")
        db.execute(sa_text("TRUNCATE TABLE primitives CASCADE"))
        db.execute(sa_text("TRUNCATE TABLE methods CASCADE"))
        db.commit()

        # 1. Seed Methods
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(current_dir, "app", "db", "seed", "seed_data_batch_3_refined.json")
        
        if not os.path.exists(json_path):
            print(f"Seed file not found: {json_path}")
            return

        with open(json_path, 'r', encoding='utf-8') as f:
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
                cross_domain_example_1=data.get('cross_domain_example_1'),
                cross_domain_example_2=data.get('cross_domain_example_2'),
                where_analogy_breaks=data.get('where_analogy_breaks'),
                assumptions=data.get('assumptions', []),
                runnable=data.get('runnable', False) == "yes" or data.get('runnable', False) is True,
                python_implementation=data.get('python_implementation'),
                tags=data.get('tags', []),
                embedding=embedding,
                complexity_level=data.get('complexity_level'),
                typical_use_cases=data.get('typical_use_cases', []),
                known_limitations=data.get('known_limitations', [])
            )
            
            db.add(method)
            db.flush() # Get the ID for the relationship if needed

            # 2. Seed Primitives if applicable
            if method.name in PRIMITIVE_REGISTRY:
                prim_inst = get_primitive_for_method(method.name)
                if prim_inst:
                    primitive = Primitive(
                        id=uuid.uuid4(),
                        name=prim_inst.name,
                        method_id=method.id,
                        method_name=method.name,
                        description=prim_inst.description,
                        input_schema=prim_inst.input_schema,
                        output_schema=prim_inst.output_schema,
                        assumptions=prim_inst.assumptions,
                        version="1.0.0",
                        active=True
                    )
                    db.add(primitive)
                    print(f"Attached primitive to: {method.name}")

            print(f"Added method: {data['name']}")

        db.commit()
        print("Seeding completed successfully.")

    except Exception as e:
        db.rollback()
        print(f"Error during seeding: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
