import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.routes import router
from app.queue.worker import worker
from app.db.init_db import init_db
from app.core.config import settings
from app.core.logger import logger
from app.repositories.job_repository import JobRepository
from app.queue.manager import job_queue


@asynccontextmanager
async def lifespan(app: FastAPI):

    await init_db()

    # Re-enqueue incomplete jobs from previous runs
    repository = JobRepository()
    incomplete_jobs = await repository.get_incomplete_jobs()

    for job in incomplete_jobs:
        if job.file_path:
            await job_queue.put({
                "id": job.id,
                "filename": job.filename,
                "file_path": job.file_path
            })
            logger.info(
                f"Re-enqueued job {job.id}"
            )
        else:
            await repository.update_job_failed(
                job.id,
                "File path missing — cannot resume after restart"
            )
            logger.warning(
                f"Marked job {job.id} as failed — no file path"
            )

    tasks = []

    for worker_id in range(
        settings.MAX_CONCURRENT_JOBS
    ):
        task = asyncio.create_task(
            worker(worker_id + 1)
        )
        tasks.append(task)

    yield

    for task in tasks:
        task.cancel()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

app.mount(
    "/frontend",
    StaticFiles(directory="frontend"),
    name="frontend"
)
