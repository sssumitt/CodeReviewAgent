# app/models.py
from sqlmodel import SQLModel, Field
from typing import Optional
import datetime

class Report(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    uuid: str = Field(index=True, unique=True)
    filename: str
    language: Optional[str] = None
    uploaded_at: datetime.datetime
    code_content: str
    review_text: Optional[str] = None
    llm_model: Optional[str] = None