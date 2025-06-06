import streamlit as st
import pandas as pd

from utils.storage import get_all_issues, save_issue

class TechLeadDashboard:
    def __init__(self):
        self.issues_df = get_all_issues()  # Should return a DataFrame

    def display_dashboard(self):
        st.title("Tech Lead Dashboard")
        st.write("Here are the issues submitted by developer interns:")

        if self.issues_df.empty:
            st.info("No issues submitted yet.")
            return

        for idx, row in self.issues_df.iterrows():
            self.display_issue(idx, row)

    def display_issue(self, idx, row):
        st.subheader(f"Issue from {row['Name']} ({row['College']})")
        st.write(f"Email: {row['Email']}")
        st.write(f"Description: {row['Description'] if 'Description' in row else row.get('Issue', '')}")
        st.write(f"Response: {row.get('Response', 'No response yet')}")
        st.write(f"Status: {'Solved' if row['Status'].lower() == 'solved' else 'Unsolved'}")

        if row['Status'].lower() == 'unsolved':
            response = st.text_area(f"Response to {row['Name']}", key=f"resp_{idx}")
            if st.button(f"Mark as Solved for {row['Name']}", key=f"solve_{idx}"):
                self.issues_df.at[idx, 'Response'] = response
                self.issues_df.at[idx, 'Status'] = 'Solved'
                save_issue(self.issues_df)
                st.success("Issue marked as solved!")