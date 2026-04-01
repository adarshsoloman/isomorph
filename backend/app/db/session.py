from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..config import settings

engine = create_engine(
    settings.DATABASE_URL,
    # pool_pre_ping is useful for catching disconnected database connections
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
