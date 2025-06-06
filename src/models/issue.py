class Issue:
    def __init__(self, name, college, email, title, description, urgency, response="", status="Unsolved"):
        self.name = name
        self.college = college
        self.email = email
        self.title = title
        self.description = description
        self.urgency = urgency
        self.response = response
        self.status = status  # "Unsolved" or "Solved"

    def update_response(self, response):
        self.response = response

    def mark_as_solved(self):
        self.status = "Solved"