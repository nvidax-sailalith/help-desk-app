from streamlit import st
from ..models.issue import Issue
from ..utils.storage import save_issue

class DeveloperForm:
    def __init__(self):
        self.name = ""
        self.college = ""
        self.email = ""
        self.description = ""

    def display_form(self):
        st.header("Developer Intern Issue Submission")
        self.name = st.text_input("Name")
        self.college = st.text_input("College")
        self.email = st.text_input("Registered Email")
        self.description = st.text_area("Issue Description")

        if st.button("Submit"):
            if self.validate_form():
                issue = Issue(self.name, self.college, self.email, self.description)
                save_issue(issue)
                st.success("Issue submitted successfully!")
            else:
                st.error("Please fill in all fields.")

    def validate_form(self):
        return all([self.name, self.college, self.email, self.description])