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
        # ----------  AVAILABLE REQUESTS  ----------

    def list_available_requests(self):
        """Επιστρέφει λίστα tuples (id, customer_id, address, people)."""
        return self.db.list_available_requests()

    def assign_request(self, request_id: int, agent_id: int) -> bool:
        """Αναθέτει το request στον agent και ενημερώνει την κατάσταση."""
        return self.db.assign_request_to_agent(request_id, agent_id)

    def list_available_requests(self):
        rows = self.db.list_available_requests()
        return [
            {"request_id": r_id, "customer_id": c_id,
             "address": addr, "people": ppl}
            for r_id, c_id, addr, ppl in rows
        ]

    def assign_request(self, request_id, agent_id):
        ok = self.db.assign_request_to_agent(request_id, agent_id)
        return (ok, "Assigned successfully." if ok else "Assignment failed.")