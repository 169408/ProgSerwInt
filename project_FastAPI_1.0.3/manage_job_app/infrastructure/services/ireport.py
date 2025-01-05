"""Module containing review service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable

from manage_job_app.core.domain.report import Report, ReportIn
from manage_job_app.infrastructure.dto.reportdto import ReportDTO


class IReportService(ABC):
    """A class representing report repository."""

    @abstractmethod
    async def get_report(self) -> Iterable[ReportDTO]:
        """The method getting reports from the repository.

        Returns:
            Iterable[ReportDTO]: report.
        """