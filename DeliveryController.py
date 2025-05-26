# DeliveryController.py
from datetime import datetime
from Database import Database

class DeliveryController:

    VALID_STATUSES = {"pending", "in_transit", "completed"}

    def __init__(self):
        self.db = Database()

    # ----------  QUERY  ----------
    def list_my_deliveries(self, agent_id):
        rows = self.db.get_agent_deliveries(agent_id)
        return [
            {"delivery_id": d_id, "request_id": r_id,
             "status": status, "eta": eta} for d_id, r_id, status, eta in rows
        ]

    # ----------  COMMAND  ----------
    def update_status(self, delivery_id, new_status, eta_str=None):
        if new_status not in self.VALID_STATUSES:
            return False, "Invalid status."

        eta = None
        if eta_str:
            try:
                eta = datetime.strptime(eta_str, "%Y-%m-%d %H:%M")
            except ValueError:
                return False, "ETA format must be YYYY-MM-DD HH:MM"

        ok = self.db.update_delivery_status(delivery_id, new_status, eta)
        return (ok, "Delivery updated." if ok else "Update failed.")
