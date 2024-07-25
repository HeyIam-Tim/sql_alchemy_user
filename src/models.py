import datetime
from typing import Optional, Annotated
from sqlalchemy import TIMESTAMP, Enum, Table, Column, Integer, String, MetaData, ForeignKey, func, text, Index, \
    CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base, str_256
import enum

intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime.datetime, mapped_column(
    server_default=text("TIMEZONE('utc', now() + interval '1 day')"),
    onupdate=datetime.datetime.utcnow,
)]


class Workload(enum.Enum):
    parttime = "parttime"
    fulltime = "fulltime"


class Worker(Base):
    __tablename__ = "worker"

    id: Mapped[intpk]
    username: Mapped[str]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    resumes: Mapped[list['Resume']] = relationship(
        back_populates='worker',
    )

    # resumes_parttime: Mapped[list['Resume']] = relationship(
    #     back_populates='worker',
    #     primaryjoin='and_(Worker.id == Resume.worker_id, Resume.workload == "parttime")',
    #     order_by='Resume.id.desc()',
    #     # lazy='selectin',
    # )


class Resume(Base):
    __tablename__ = "resume"

    id: Mapped[intpk]
    title: Mapped[str_256]
    # compensation: Mapped[int | None]
    compensation: Mapped[float]
    workload: Mapped[Workload]
    worker_id: Mapped[int] = mapped_column(ForeignKey("worker.id", ondelete="CASCADE"))
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    worker: Mapped['Worker'] = relationship(
        back_populates='resumes',
    )

    statuses: Mapped[list['Status']] = relationship(
        back_populates='resume',
    )

    vacancies_replied: Mapped[list['Vacancy']] = relationship(
        back_populates='resumes_replied',
        secondary='vacancy_replies',
    )

    repr_cols_num = 5
    repr_cols = ('title', )

    __table_args__ = (
        Index('title_index', 'title'),
        CheckConstraint('compensation > 0', name='check_compensation_gt')
    )


class Vacancy(Base):
    __tablename__ = 'vacancy'

    id: Mapped[intpk]
    title: Mapped[str_256]
    compensation: Mapped[int | None]

    resumes_replied: Mapped[list['Resume']] = relationship(
        back_populates='vacancies_replied',
        secondary='vacancy_replies',
    )


class VacancyReplies(Base):
    __tablename__ = 'vacancy_replies'

    resume_id: Mapped[int] = mapped_column(
        ForeignKey('resume.id', ondelete='CASCADE'),
        primary_key=True,
    )
    vacancy_id: Mapped[int] = mapped_column(
        ForeignKey('vacancy.id', ondelete='CASCADE'),
        primary_key=True,
    )

    cover_letter: Mapped[str | None]


class StatusStates(enum.Enum):
    """Состояния статусов"""

    active = 'active'
    inactive = 'inactive'
    pending = 'pending'
    new = 'new'


class Status(Base):
    """Статус"""

    __tablename__ = 'status'

    id: Mapped[intpk]
    resume_id: Mapped[int] = mapped_column(ForeignKey("resume.id", ondelete="CASCADE"))
    state: Mapped[StatusStates]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    resume: Mapped['Resume'] = relationship(
        back_populates='statuses',
    )


metadata_obj = MetaData()

worker_table = Table(
    "worker",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("username", String),
)


resume_table = Table(
    "resume",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("title", String(256)),
    Column("compensation", Integer, nullable=True),
    Column("workload", Enum(Workload)),
    Column("worker_id", ForeignKey("worker.id", ondelete="CASCADE")),
    Column("created_at", TIMESTAMP, server_default=text("TIMEZONE('utc', now())")),
    Column("updated_at", TIMESTAMP, server_default=text("TIMEZONE('utc', now())"), onupdate=datetime.datetime.utcnow),
)
