"""Module containing report repository abstractions."""

from abc import ABC, abstractmethod
from typing import Any, Iterable

from manage_job_app.core.domain.report import ReportIn


class IReportRepository(ABC):
    """An abstract class representing protocol of report repository."""

    @abstractmethod
    async def get_report(self) -> Iterable[Any]:
        """The abstract getting report.

        Returns:
            Iterable[Report]: Report.
        """
