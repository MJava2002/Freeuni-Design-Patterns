from dataclasses import dataclass, field
from uuid import UUID

from core.services import Report


@dataclass
class ReportInMemory:
    report: dict[UUID, Report] = field(default_factory=dict)

    def create(self, reports: Report) -> None:
        self.report[reports.id] = reports

    def read_report(self, report_id: UUID) -> Report:
        return self.report[report_id]
