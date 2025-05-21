class Report:
    def __init__(self, author, date_created):
        self.author = author
        self.date_created = date_created
        self.content = ""
        self.last_modified = date_created