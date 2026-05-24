from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime
)

from datetime import datetime, timezone

from app.db.database import Base


class JobTable(Base):

    __tablename__ = "jobs"

    id = Column(
        String,
        primary_key=True
    )

    filename = Column(
        String,
        nullable=False
    )

    status = Column(
        String,
        nullable=False
    )

    retry_count = Column(
        Integer,
        default=0
    )

    error_message = Column(
        String,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(
            timezone.utc
        )
    )

    started_at = Column(
        DateTime,
        nullable=True
    )

    completed_at = Column(
        DateTime,
        nullable=True
    )

    summary = Column(
        String,
        nullable=True
    )

    file_path = Column(
        String,
        nullable=True
    )

    summary_file = Column(
        String,
        nullable=True
    )
