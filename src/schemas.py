from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from .models import Workload, StatusStates


class WorkersAddDTO(BaseModel):
    username: str


class WorkersDTO(WorkersAddDTO):
    id: int


class ResumesAddDTO(BaseModel):
    title: str
    compensation: Optional[int]
    workload: Workload
    worker_id: int


class ResumesDTO(ResumesAddDTO):
    id: int
    created_at: datetime
    updated_at: datetime


class StatusDTO(BaseModel):
    id: int
    # resume_id: int
    state: StatusStates
    created_at: datetime
    updated_at: datetime


class ResumesRelDTO(ResumesDTO):
    worker: "WorkersDTO"
    statuses: list['StatusDTO']


class WorkersRelDTO(WorkersDTO):
    resumes: list["ResumesDTO"]


class WorkloadAvgCompensationDTO(BaseModel):
    workload: str
    avg_compensation: int


class VacanciesAddDTO(BaseModel):
    title: str
    compensation: Optional[int]


class VacanciesDTO(VacanciesAddDTO):
    id: int


class VacanciesWithoutCompensationDTO(BaseModel):
    id: int
    title: str


class ResumesRelVacanciesRepliedDTO(ResumesDTO):
    worker: "WorkersDTO"
    vacancies_replied: list["VacanciesDTO"]


class ResumesRelVacanciesRepliedWithoutVacancyCompensationDTO(ResumesDTO):
    worker: "WorkersDTO"
    vacancies_replied: list["VacanciesWithoutCompensationDTO"]
