from pydantic import BaseModel

from enum import Enum

class JobStatus(str, Enum):

    QUEUED = "queued"

    EXTRACTING = "extracting_pdf"

    SUMMARIZING = "summarizing"

    GENERATING_DOCX = "generating_docx"

    COMPLETED = "completed"

    FAILED = "failed"


class CreateJobRequest(BaseModel):

    filename: str


class JobResponse(BaseModel):

    id: str

    filename: str

    status: JobStatus
