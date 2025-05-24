# StatisticsReportController.py
from datetime import datetime
from Database import Database
from Report import Report


class StatisticsReportController:
    """Συγκεντρώνει στατιστικά από τη βάση και χτίζει αναφορά."""

    def __init__(self):
        self.db = Database()

    # ----------  ΣΥΛΛΟΓΗ ΣΤΑΤΙΣΤΙΚΩΝ  ----------
    def _query_scalar(self, sql, params=None, fallback=0):
        """Εκτελεί query που επιστρέφει single-value (π.χ. COUNT)."""
        res = self.db.execute_query(sql, params)
        return res[0][0] if res else fallback

    def fetch_statistics(self):
        """Επιστρέφει dict με όλα τα απαιτούμενα νούμερα."""
        stats = {
            # Χρήστες
            "total_users": self._query_scalar("SELECT COUNT(*) FROM users"),
            "users_per_role": {
                role: cnt
                for role, cnt in (
                    self.db.execute_query(
                        "SELECT role, COUNT(*) FROM users GROUP BY role"
                    )
                    or []
                )
            },
            # Δωρεές
            "total_donations": self._query_scalar("SELECT COUNT(*) FROM donations"),
            "total_items_donated": self._query_scalar(
                "SELECT IFNULL(SUM(quantity),0) FROM donations"
            ),
            # Αιτήματα τροφίμων
            "total_requests": self._query_scalar("SELECT COUNT(*) FROM food_requests"),
            "requests_by_status": {
                status: cnt
                for status, cnt in (
                    self.db.execute_query(
                        "SELECT status, COUNT(*) FROM food_requests GROUP BY status"
                    )
                    or []
                )
            },
        }
        return stats

    # ----------  ΔΗΜΙΟΥΡΓΙΑ ΑΝΑΦΟΡΑΣ  ----------
    def build_report(self, admin_id):
        """Επιστρέφει αντικείμενο Report ή None αν δεν υπάρχουν δεδομένα."""
        stats = self.fetch_statistics()

        nothing_to_show = (
            stats["total_users"] == 0
            and stats["total_donations"] == 0
            and stats["total_requests"] == 0
        )
        if nothing_to_show:
            return None  # Ενεργοποιεί την εναλλακτική ροή 2.1

        lines = [
            f"=== Statistics Report ({datetime.now():%Y-%m-%d %H:%M}) ===\n",
            f"Total registered users: {stats['total_users']}",
        ]
        if stats["users_per_role"]:
            lines.append("Users per role:")
            for role, cnt in stats["users_per_role"].items():
                lines.append(f"   • {role}: {cnt}")

        lines.extend(
            [
                "",
                f"Total donations made: {stats['total_donations']}",
                f"Total individual items donated: {stats['total_items_donated']}",
                "",
                f"Total food requests: {stats['total_requests']}",
            ]
        )
        if stats["requests_by_status"]:
            lines.append("Requests by status:")
            for status, cnt in stats["requests_by_status"].items():
                lines.append(f"   • {status}: {cnt}")

        # Δημιουργία αντικειμένου Report
        rpt = Report(author=admin_id, date_created=datetime.now())
        rpt.content = "\n".join(lines)
        return rpt
