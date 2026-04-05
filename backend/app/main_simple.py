from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os
import uuid
import aiofiles
from datetime import datetime

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./document_processor.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    original_filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    upload_time = Column(DateTime, default=datetime.utcnow)

class ProcessingJob(Base):
    __tablename__ = "processing_jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, nullable=False)
    status = Column(String, default="queued", nullable=False)
    progress_percentage = Column(Float, default=0.0)
    current_stage = Column(String, default="queued")
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    extracted_title = Column(Text, nullable=True)
    extracted_category = Column(String, nullable=True)
    extracted_summary = Column(Text, nullable=True)
    extracted_keywords = Column(Text, nullable=True)  # JSON as text
    processed_content = Column(Text, nullable=True)
    final_result = Column(Text, nullable=True)  # JSON as text
    is_reviewed = Column(String, default=False)
    is_finalized = Column(String, default=False)
    celery_task_id = Column(String, nullable=True)

# Create tables
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# FastAPI app
app = FastAPI(
    title="Document Processing System",
    version="1.0.0",
    description="Async document processing workflow system"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Upload directory
UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/api/v1/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload a document and create a processing job"""
    
    # Validate file
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    # Generate unique filename
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    # Save file
    async with aiofiles.open(file_path, 'wb') as f:
        content = await file.read()
        await f.write(content)
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Create document record
        document = Document(
            filename=unique_filename,
            original_filename=file.filename,
            file_path=file_path,
            file_type=file.content_type or "unknown",
            file_size=len(content)
        )
        
        db.add(document)
        db.commit()
        db.refresh(document)
        
        # Create processing job
        processing_job = ProcessingJob(
            document_id=document.id,
            status="queued"
        )
        
        db.add(processing_job)
        db.commit()
        db.refresh(processing_job)
        
        # Simulate processing (in real implementation, this would be a Celery task)
        processing_job.status = "completed"
        processing_job.progress_percentage = 100.0
        processing_job.current_stage = "completed"
        processing_job.extracted_title = file.filename
        processing_job.extracted_category = "General"
        processing_job.extracted_summary = f"Processed document: {file.filename}"
        processing_job.extracted_keywords = '["document", "processing"]'
        processing_job.completed_at = datetime.utcnow()
        
        db.commit()
        db.refresh(processing_job)
        
        return processing_job
        
    finally:
        db.close()

@app.get("/api/v1/jobs")
async def list_jobs(skip: int = 0, limit: int = 100):
    """List all processing jobs"""
    db = SessionLocal()
    try:
        jobs = db.query(ProcessingJob).offset(skip).limit(limit).all()
        
        # Convert to dict for JSON response
        result = []
        for job in jobs:
            job_dict = {
                "id": job.id,
                "document_id": job.document_id,
                "status": job.status,
                "progress_percentage": job.progress_percentage,
                "current_stage": job.current_stage,
                "error_message": job.error_message,
                "created_at": job.created_at.isoformat() if job.created_at else None,
                "started_at": job.started_at.isoformat() if job.started_at else None,
                "completed_at": job.completed_at.isoformat() if job.completed_at else None,
                "extracted_title": job.extracted_title,
                "extracted_category": job.extracted_category,
                "extracted_summary": job.extracted_summary,
                "extracted_keywords": eval(job.extracted_keywords) if job.extracted_keywords else [],
                "processed_content": job.processed_content,
                "final_result": eval(job.final_result) if job.final_result else None,
                "is_reviewed": job.is_reviewed,
                "is_finalized": job.is_finalized,
                "celery_task_id": job.celery_task_id
            }
            result.append(job_dict)
        
        return result
        
    finally:
        db.close()

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main_simple:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
