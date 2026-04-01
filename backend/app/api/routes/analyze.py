from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...db.session import get_db
from ...schemas.analogy import AnalysisRequest, AnalysisResponse
from ...core.pipeline import Pipeline

router = APIRouter()

@router.post("/", response_model=AnalysisResponse)
async def analyze_problem(
    request: AnalysisRequest, 
    db: Session = Depends(get_db)
):
    """
    The main ISOMORPH structural analogy endpoint.
    Takes raw text, returns scored analogies and mathematical mappings.
    """
    pipeline = Pipeline(db)
    try:
        response = pipeline.run(request.input_text)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
