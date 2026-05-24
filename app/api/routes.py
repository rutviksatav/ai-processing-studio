from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException
)

from uuid import uuid4

import os

from app.queue.manager import job_queue

from app.repositories.job_repository import (
    JobRepository
)

from app.schemas.job import JobStatus

from fastapi.responses import FileResponse

router = APIRouter()

repository = JobRepository()


UPLOAD_DIR = "uploads"

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)


@router.post("/jobs")
async def create_job(
    file: UploadFile = File(...)
):

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are accepted"
        )

    content = await file.read()

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File size exceeds 50 MB limit"
        )

    job_id = str(uuid4())

    safe_filename = os.path.basename(
        file.filename
    )

    file_path = (
        f"{UPLOAD_DIR}/{job_id}_{safe_filename}"
    )

    with open(file_path, "wb") as f:
        f.write(content)


    await repository.create_job(
        job_id=job_id,
        filename=safe_filename,
        status=JobStatus.QUEUED.value,
        file_path=file_path
    )


    await job_queue.put({

        "id": job_id,

        "filename": safe_filename,

        "file_path": file_path
    })


    return {
        "message": "PDF uploaded",
        "job_id": job_id
    }


@router.get("/jobs")
async def get_jobs():

    jobs = await repository.get_all_jobs()

    return [
        {
            "id": job.id,
            "filename": job.filename,
            "status": job.status,
            "summary_file": job.summary_file
        }
        for job in jobs
    ]


@router.get("/jobs/{job_id}/download")
async def download_summary(
    job_id: str
):

    job = await repository.get_job_by_id(
        job_id
    )

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    if not job.summary_file:
        raise HTTPException(
            status_code=400,
            detail="Summary not ready yet"
        )

    clean_name = (
        job.filename
        .replace(".pdf", "")
    )


    return FileResponse(
        path=job.summary_file,

        filename=f"{clean_name}_summary.docx",

        media_type=(
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    )
