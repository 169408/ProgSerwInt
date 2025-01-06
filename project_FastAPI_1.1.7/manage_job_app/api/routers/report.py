"""A module containing report endpoints."""

from typing import Iterable
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt

from pydantic import UUID4

from manage_job_app.infrastructure.utils import consts
from manage_job_app.container import Container
from manage_job_app.core.domain.report import Report, ReportIn
from manage_job_app.infrastructure.dto.reportdto import ReportDTO
from manage_job_app.infrastructure.services.ireport import IReportService


bearer_scheme = HTTPBearer()

router = APIRouter(tags=["Reports"])
# Iterable[ReportDTO]
@router.get("/report", response_model=None, status_code=200)
@inject
async def get_report(
    service: IReportService = Depends(Provide[Container.report_service]),
) -> Iterable:
    """An endpoint for getting report.

    Args:
        service (IReportService): The injected service dependency.

    Returns:
        Iterable: The report attributes collection.
    """

    report = await service.get_report()

    return report

