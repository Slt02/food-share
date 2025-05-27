# Report.py
from __future__ import annotations
from datetime import datetime


class Report:
    """
    Γενική αναφορά (feedback, στατιστικά, κ.λπ.)
    """

    def __init__(
        self,
        request_id: int | None = None,
        customer_id: int | None = None,
        description: str = "",
        created_at: datetime | None = None,
        report_id: int | None = None,
        author: int | None = None,          # NEW
        date_created: datetime | None = None,  # NEW
    ) -> None:
        self.report_id = report_id
        self.request_id = request_id
        self.customer_id = customer_id
        self.description = description
        self.author = author                # NEW
        self.date_created = date_created or created_at or datetime.now()  # NEW
        self.content: str = ""

    # βοηθητική εμφάνιση για debug
    def __repr__(self) -> str:  
        return (
            f"<Report id={self.report_id} author={self.author} "
            f"created={self.date_created:%Y-%m-%d %H:%M:%S}>"
        )
