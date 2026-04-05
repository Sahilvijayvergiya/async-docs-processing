from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Document Processing System API"}

@app.get("/api/v1/jobs")
async def list_jobs():
    return [
        {
            "id": 1,
            "document_id": 1,
            "status": "completed",
            "progress_percentage": 100.0,
            "current_stage": "completed",
            "error_message": None,
            "created_at": "2024-01-01T00:00:00",
            "started_at": "2024-01-01T00:01:00",
            "completed_at": "2024-01-01T00:02:00",
            "extracted_title": "Sample Document",
            "extracted_category": "General",
            "extracted_summary": "This is a sample processed document",
            "extracted_keywords": ["sample", "document"],
            "processed_content": "Sample content...",
            "final_result": {"title": "Sample Document"},
            "is_reviewed": False,
            "is_finalized": False,
            "celery_task_id": None,
            "document": {
                "id": 1,
                "filename": "sample.txt",
                "original_filename": "sample.txt",
                "file_type": "text/plain",
                "file_size": 1024,
                "upload_time": "2024-01-01T00:00:00"
            }
        }
    ]

@app.get("/api/v1/jobs/{job_id}")
async def get_job(job_id: int):
    return {
        "id": job_id,
        "document_id": 1,
        "status": "completed",
        "progress_percentage": 100.0,
        "current_stage": "completed",
        "error_message": None,
        "created_at": "2024-01-01T00:00:00",
        "started_at": "2024-01-01T00:01:00",
        "completed_at": "2024-01-01T00:02:00",
        "extracted_title": "Sample Document",
        "extracted_category": "General",
        "extracted_summary": "This is a sample processed document",
        "extracted_keywords": ["sample", "document"],
        "processed_content": "Sample content...",
        "final_result": {"title": "Sample Document"},
        "is_reviewed": False,
        "is_finalized": False,
        "celery_task_id": None,
        "document": {
            "id": 1,
            "filename": "sample.txt",
            "original_filename": "sample.txt",
            "file_type": "text/plain",
            "file_size": 1024,
            "upload_time": "2024-01-01T00:00:00"
        }
    }

@app.put("/api/v1/jobs/{job_id}")
async def update_job(job_id: int, request_data: dict):
    return {
        "id": job_id,
        "document_id": 1,
        "status": "completed",
        "progress_percentage": 100.0,
        "current_stage": "completed",
        "error_message": None,
        "created_at": "2024-01-01T00:00:00",
        "started_at": "2024-01-01T00:01:00",
        "completed_at": "2024-01-01T00:02:00",
        "extracted_title": request_data.get("extracted_title", "Sample Document"),
        "extracted_category": request_data.get("extracted_category", "General"),
        "extracted_summary": request_data.get("extracted_summary", "This is a sample processed document"),
        "extracted_keywords": request_data.get("extracted_keywords", ["sample", "document"]),
        "processed_content": "Sample content...",
        "final_result": request_data.get("final_result", {"title": "Sample Document"}),
        "is_reviewed": request_data.get("is_reviewed", False),
        "is_finalized": request_data.get("is_finalized", False),
        "celery_task_id": None,
        "document": {
            "id": 1,
            "filename": "sample.txt",
            "original_filename": "sample.txt",
            "file_type": "text/plain",
            "file_size": 1024,
            "upload_time": "2024-01-01T00:00:00"
        }
    }

@app.post("/api/v1/jobs/{job_id}/retry")
async def retry_job(job_id: int):
    return {
        "id": job_id,
        "document_id": 1,
        "status": "queued",
        "progress_percentage": 0.0,
        "current_stage": "queued",
        "error_message": None,
        "created_at": "2024-01-01T00:00:00",
        "started_at": None,
        "completed_at": None,
        "extracted_title": "Sample Document",
        "extracted_category": "General",
        "extracted_summary": "This is a sample processed document",
        "extracted_keywords": ["sample", "document"],
        "processed_content": "Sample content...",
        "final_result": {"title": "Sample Document"},
        "is_reviewed": False,
        "is_finalized": False,
        "celery_task_id": "new_task_id",
        "document": {
            "id": 1,
            "filename": "sample.txt",
            "original_filename": "sample.txt",
            "file_type": "text/plain",
            "file_size": 1024,
            "upload_time": "2024-01-01T00:00:00"
        }
    }

@app.post("/api/v1/jobs/{job_id}/finalize")
async def finalize_job(job_id: int):
    return {"message": "Job finalized successfully"}

@app.get("/api/v1/jobs/export/json")
async def export_json():
    data = [
        {
            "id": 1,
            "document_filename": "sample.txt",
            "status": "completed",
            "extracted_title": "Sample Document",
            "extracted_category": "General",
            "extracted_summary": "This is a sample processed document",
            "extracted_keywords": ["sample", "document"],
            "created_at": "2024-01-01T00:00:00",
            "completed_at": "2024-01-01T00:02:00"
        }
    ]
    
    return JSONResponse(
        content=json.dumps(data, indent=2),
        media_type="application/json",
        headers={"Content-Disposition": "attachment; filename=jobs_export.json"}
    )

@app.get("/api/v1/jobs/export/csv")
async def export_csv():
    csv_data = """ID,Document Filename,Status,Title,Category,Summary,Keywords,Created At,Completed At
1,sample.txt,completed,Sample Document,General,"This is a sample processed document","sample;document",2024-01-01T00:00:00,2024-01-01T00:02:00
"""
    
    return JSONResponse(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=jobs_export.csv"}
    )

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
