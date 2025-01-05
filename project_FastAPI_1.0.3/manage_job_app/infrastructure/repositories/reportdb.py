"""Module containing report repository implementation."""
from datetime import datetime, timedelta
from pyexpat.errors import messages
from typing import Any, Iterable

from asyncpg import Record  # type: ignore
from sqlalchemy import select, join, alias, func

from manage_job_app.core.repositories.ireport import IReportRepository
from manage_job_app.core.domain.report import Report, ReportIn
from manage_job_app.db import (
    offer_table,
    database,
)
from manage_job_app.infrastructure.dto.reportdto import ReportDTO


class ReportRepository(IReportRepository):
    """A class representing report DB repository."""

    async def get_report(self) -> ReportDTO:
        """The method getting report.

        Returns:
            Iterable[Any]: Report in the data storage.
        """

        now = datetime.utcnow()
        last_day = now - timedelta(days=1)
        last_week = now - timedelta(weeks=1)
        last_month = now - timedelta(days=30)

        print(last_day)
        print(last_week)
        print(last_month)

        query_day = select(func.count()).where(offer_table.c.created_at >= last_day)
        query_week = select(func.count()).where(offer_table.c.created_at >= last_week)
        query_month = select(func.count()).where(offer_table.c.created_at >= last_month)

        day_count = await database.fetch_val(query_day)
        week_count = await database.fetch_val(query_week)
        month_count = await database.fetch_val(query_month)

        fake_record = {
            "topic": "Offer Counts Report",
            "content": (
                f"offers_last_day: {day_count}, "
                f"offers_last_week: {week_count}, "
                f"offers_last_month: {month_count}"
            ),
        }

        #fake_obj_record = Report(**dict(fake_record))

        return ReportDTO.from_record(fake_record)