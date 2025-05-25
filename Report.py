class Report:
    def __init__(self, request_id, customer_id, description, created_at=None, report_id=None):
        self.report_id = report_id
        self.customer_id = customer_id
        self.description = description
        self.request_id = request_id
        self.created_at = created_at
