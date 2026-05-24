from app.queue.manager import job_queue

from app.services.document_processor import (
    process_document
)

from app.repositories.job_repository import (
    JobRepository
)

from app.core.logger import logger


repository = JobRepository()


async def worker(worker_id: int):

    logger.info(
        f"Worker-{worker_id} started"
    )

    while True:

        job = await job_queue.get()

        try:

            logger.info(
                f"Worker-{worker_id} processing "
                f"{job['id']}"
            )

            await repository.update_job_processing(
                job["id"]
            )

            await process_document(
                job["id"],
                job["filename"],
                job["file_path"]
            )

            logger.info(
                f"Worker-{worker_id} completed "
                f"{job['id']}"
            )

        except Exception as e:

            logger.error(str(e))

            await repository.update_job_failed(
                job["id"],
                str(e)
            )

        finally:

            job_queue.task_done()
