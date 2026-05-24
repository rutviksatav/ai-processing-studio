import os

from app.services.pdf_service import (
    extract_pdf_text
)

from app.services.llm_service import (
    generate_summary
)

from app.services.file_service import (
    save_summary_file
)

from app.repositories.job_repository import (
    JobRepository
)

from app.schemas.job import JobStatus

from app.core.logger import logger


repository = JobRepository()



async def process_document(
    job_id: str,
    filename: str,
    file_path: str
):

    logger.info(
        f"Extracting PDF: {job_id}"
    )

    await repository.update_status(
        job_id,
        JobStatus.EXTRACTING.value
    )

    text = await extract_pdf_text(
        file_path
    )

    # Clean up uploaded PDF — text is extracted, file no longer needed
    try:
        os.remove(file_path)
        logger.info(
            f"Cleaned up upload: {file_path}"
        )
    except OSError:
        pass


    logger.info(
        f"Generating summary: {job_id}"
    )

    await repository.update_status(
        job_id,
        JobStatus.SUMMARIZING.value
    )

    summary = await generate_summary(
        text
    )


    logger.info(
        f"Generating DOCX: {job_id}"
    )

    await repository.update_status(
        job_id,
        JobStatus.GENERATING_DOCX.value
    )

    generated_file = await save_summary_file(
        job_id,
        filename,
        summary
    )


    await repository.save_summary_file(
        job_id,
        generated_file
    )


    await repository.update_status(
        job_id,
        JobStatus.COMPLETED.value
    )


    logger.info(
        f"Completed summary: {job_id}"
    )
