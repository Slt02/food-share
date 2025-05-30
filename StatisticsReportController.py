# StatisticsReportController.py
from __future__ import annotations
from datetime import datetime
from typing import Dict, Any
from Database import Database
from Report import Report


class StatisticsReportController:
    """Δημιουργεί στατιστικές και (προαιρετικά) τις αποθηκεύει."""

    def __init__(self, db: Database | None = None) -> None:
        self.db: Database = db or Database()

    
    def _single_value(self, sql: str, params: tuple = ()) -> int:
        rows = self.db.execute_query(sql, params or ())  # returns list[tuple]
        return int(rows[0][0]) if rows else 0

    def _count(self, table: str, where: str | None = None) -> int:
        q = f"SELECT COUNT(*) FROM {table}"
        if where:
            q += " WHERE " + where
        return self._single_value(q)

    def collect_kpis(self) -> Dict[str, Any]:
        return {
            "users_total":        self._count("users"),
            "customers":          self._count("users", "role='customer'"),
            "donors":             self._count("users", "role='donor'"),
            "dropoff_agents":     self._count("users", "role='drop_off_agent'"),
            "pending_requests":   self._count("food_requests", "status='pending'"),
            "in_transit_requests":self._count("food_requests", "status='in_transit'"),
            "completed_requests": self._count("food_requests", "status='completed'"),
            "donations":          self._count("donations"),
        }

    def build_report(self, admin_id: int) -> Report | None:
        """Επιστρέφει έτοιμο Report ή None αν δεν υπάρχουν δεδομένα."""
        stats = self.collect_kpis()
        if not stats:
            return None

        now = datetime.now()
        lines = [
            "FoodShare – Daily Statistics Report",
            f"Generated: {now:%Y-%m-%d %H:%M:%S}",
            f"Admin ID : {admin_id}",
            "",
            "=== Users ===",
            f"Total           : {stats['users_total']}",
            f"  • Customers   : {stats['customers']}",
            f"  • Donors      : {stats['donors']}",
            f"  • Drop-off Ag.: {stats['dropoff_agents']}",
            "",
            "=== Food Requests ===",
            f"Pending         : {stats['pending_requests']}",
            f"In transit      : {stats['in_transit_requests']}",
            f"Completed       : {stats['completed_requests']}",
            "",
            "=== Donations ===",
            f"Total donations : {stats['donations']}",
            "",
            "End of report.",
        ]

        rpt = Report(
            description="Daily statistics report",
            created_at=now,
            author=admin_id,
            date_created=now,
        )
        rpt.content = "\n".join(lines)
        return rpt

    def save_report(self, report: Report) -> bool:
        sql = (
            "INSERT INTO reports (author_id, description, content, created_at) "
            "VALUES (%s, %s, %s, %s)"
        )
        params = (report.author, report.description, report.content, report.date_created)
        try:
            self.db.execute_query(sql, params)
            self.db.connection.commit()
            return True
        except Exception as err:
            print("[StatisticsReportController] save_report failed:", err)
            return False

