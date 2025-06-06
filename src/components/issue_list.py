import streamlit as st

def display_issue_list(issues_df):
    st.title("Issue List")

    if issues_df.empty:
        st.write("No issues submitted yet.")
        return

    for idx, row in issues_df.iterrows():
        st.subheader(f"Issue from {row['Name']} ({row['College']})")
        st.write(f"Email: {row['Email']}")
        st.write(f"Description: {row['Description'] if 'Description' in row else row.get('Issue', '')}")
        st.write(f"Status: {'Solved' if row['Status'].lower() == 'solved' else 'Unsolved'}")
        
        if row.get('Response', ''):
            st.write(f"Response: {row['Response']}")
        
        if row['Status'].lower() == 'unsolved':
            response = st.text_area(f"Response to {row['Name']}", key=f"resp_{idx}")
            if st.button(f"Mark as Solved for {row['Name']}", key=f"solve_{idx}"):
                issues_df.at[idx, 'Response'] = response
                issues_df.at[idx, 'Status'] = 'Solved'
                st.success("Issue marked as solved!")