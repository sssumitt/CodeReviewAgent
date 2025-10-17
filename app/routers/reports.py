# app/routers/reports.py
from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlmodel import Session, select
import uuid
import datetime

from ..database import get_session
from ..models import Report
from ..services import call_gemini_review
from ..utils import language_from_filename

router = APIRouter()

@router.post("/review-file")
async def review_file(
    session: Session = Depends(get_session),
    file: UploadFile = File(...),
    model: str = Form('gemini-2.5-pro')
):
    content = await file.read()
    try:
        text = content.decode('utf-8')
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="Unable to decode file as UTF-8 text.")

    language = language_from_filename(file.filename)
    review_uuid = str(uuid.uuid4())

    report = Report(
        uuid=review_uuid,
        filename=file.filename,
        language=language,
        uploaded_at=datetime.datetime.utcnow(),
        code_content=text,
        llm_model=model,
    )
    session.add(report)
    session.commit()

    try:
        review_text = call_gemini_review(text, file.filename, model_name=model)
        report.review_text = review_text
    except Exception as e:
        report.review_text = f"Review failed: {e}"
        session.add(report)
        session.commit()
        raise HTTPException(status_code=500, detail=str(e))

    session.add(report)
    session.commit()

    return JSONResponse({
        "uuid": report.uuid,
        "filename": report.filename,
        "language": report.language,
        "review": report.review_text,
    })


@router.get("/reports", response_model=list[dict])
def list_reports(limit: int = 20, session: Session = Depends(get_session)):
    stmt = select(Report).order_by(Report.uploaded_at.desc()).limit(limit)
    results = session.exec(stmt).all()
    return [
        {
            "uuid": r.uuid,
            "filename": r.filename,
            "language": r.language,
            "uploaded_at": r.uploaded_at.isoformat(),
            "snippet": (r.review_text[:200] + '...') if r.review_text else None,
        }
        for r in results
    ]

@router.get("/report/{report_uuid}", response_model=Report)
def get_report(report_uuid: str, session: Session = Depends(get_session)):
    stmt = select(Report).where(Report.uuid == report_uuid)
    report = session.exec(stmt).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report