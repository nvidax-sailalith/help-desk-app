import pandas as pd
import os

ISSUES_CSV = "issues.csv"

def save_issue(issues_df):
    # issues_df: pandas DataFrame with all issues
    issues_df.to_csv(ISSUES_CSV, index=False)

def get_all_issues():
    if os.path.exists(ISSUES_CSV):
        return pd.read_csv(ISSUES_CSV)
    else:
        # Return an empty DataFrame with expected columns
        return pd.DataFrame(columns=[
            "ID", "Name", "Email", "College", "Title", "Description",
            "Urgency", "Status", "Timestamp", "ResolvedBy", "Response"
        ])