from sqlalchemy import select

from datetime import datetime, timezone

from app.db.database import AsyncSessionLocal

from app.db.models import JobTable

from app.schemas.job import JobStatus


class JobRepository:


    async def create_job(
        self,
        job_id: str,
        filename: str,
        status: str,
        file_path: str = None
    ):

        async with AsyncSessionLocal() as session:

            job = JobTable(
                id=job_id,
                filename=filename,
                status=status,
                file_path=file_path
            )

            session.add(job)

            await session.commit()

            return job


    async def get_job_by_id(
        self,
        job_id: str
    ):

        async with AsyncSessionLocal() as session:

            query = select(JobTable).where(
                JobTable.id == job_id
            )

            result = await session.execute(query)

            return result.scalar_one_or_none()


    async def update_job_processing(
        self,
        job_id: str
    ):

        async with AsyncSessionLocal() as session:

            query = select(JobTable).where(
                JobTable.id == job_id
            )

            result = await session.execute(query)

            job = result.scalar_one()

            job.status = JobStatus.EXTRACTING.value

            job.started_at = datetime.now(
                timezone.utc
            )

            await session.commit()


    async def update_job_failed(
        self,
        job_id: str,
        error_message: str
    ):

        async with AsyncSessionLocal() as session:

            query = select(JobTable).where(
                JobTable.id == job_id
            )

            result = await session.execute(query)

            job = result.scalar_one()

            job.status = JobStatus.FAILED.value

            job.error_message = error_message

            job.retry_count += 1

            await session.commit()


    async def get_all_jobs(self):

        async with AsyncSessionLocal() as session:

            query = select(JobTable)

            result = await session.execute(query)

            return result.scalars().all()


    async def save_summary_file(
        self,
        job_id: str,
        file_path: str
    ):

        async with AsyncSessionLocal() as session:

            query = select(JobTable).where(
                JobTable.id == job_id
            )

            result = await session.execute(query)

            job = result.scalar_one()

            job.summary_file = file_path

            await session.commit()


    async def update_status(
        self,
        job_id: str,
        status: str
    ):

        async with AsyncSessionLocal() as session:

            query = select(JobTable).where(
                JobTable.id == job_id
            )

            result = await session.execute(query)

            job = result.scalar_one()

            job.status = status

            await session.commit()


    async def get_incomplete_jobs(self):

        async with AsyncSessionLocal() as session:

            query = select(JobTable).where(
                JobTable.status.notin_([
                    JobStatus.COMPLETED.value,
                    JobStatus.FAILED.value
                ])
            )

            result = await session.execute(query)

            return result.scalars().all()
