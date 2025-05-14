class Report:
    def __init__(self, report_id, author, date_created):
        self.report_id = report_id
        self.author = author
        self.date_created = date_created
        self.content = ""
        self.last_modified = date_created