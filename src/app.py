import streamlit as st
import pandas as pd
from datetime import datetime
import altair as alt
import os

# ─── CONSTANTS ──────────────────────────────────────────────────────────────────
USERS_CSV = "users.csv"
ISSUES_CSV = "issues.csv"

# ─── USER MANAGEMENT HELPERS ───────────────────────────────────────────────────

def load_users():
    if os.path.exists(USERS_CSV):
        return pd.read_csv(USERS_CSV)
    else:
        return pd.DataFrame(columns=["email", "password", "role"])

def save_user(email, password, role):
    users_df = load_users()
    if email in users_df["email"].values:
        return False  # Already registered
    new_user = pd.DataFrame([[email, password, role]], columns=["email", "password", "role"])
    updated_df = pd.concat([users_df, new_user], ignore_index=True)
    updated_df.to_csv(USERS_CSV, index=False)
    return True

# ─── STREAMLIT PAGE CONFIG ─────────────────────────────────────────────────────

st.set_page_config(
    page_title="ResolveHub",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ─── CUSTOM DARK MODE STYLES (RED / ORANGE THEME) ───────────────────────────────

st.markdown(
    """
    <style>
    body, .main, .stApp {
        background-color: #1f0b0b !important;  /* Very dark red/brown */
    }
    .stApp {
        font-family: 'Segoe UI', 'Roboto', sans-serif;
        color: #ffece0 !important;             /* Light cream text */
    }
    .resolve-header {
        background: linear-gradient(90deg, #660000 0%, #990000 100%);  /* Dark red gradient */
        border-radius: 18px;
        padding: 2.5rem 1rem 2rem 1rem;
        margin-bottom: 2.5rem;
        box-shadow: 0 6px 32px 0 rgba(20, 10, 10, 0.5);
    }
    .resolve-header h1 {
        color: #fff1e0;                       /* Soft cream */
        font-size: 3.2rem;
        font-family: 'Segoe UI', 'Roboto', sans-serif;
        letter-spacing: 2px;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .resolve-header p {
        color: #ffd1a4;                       /* Pale orange */
        font-size: 1.25rem;
        text-align: center;
        margin-top: 0;
    }
    .stButton>button, .stFormSubmitButton>button {
        background: linear-gradient(90deg, #ff4500 0%, #cc3300 100%) !important;  /* Bright orange to dark red */
        color: #ffffff !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 0.5rem 1.5rem !important;
        border: none !important;
        transition: background 0.2s;
        box-shadow: 0 2px 8px 0 rgba(44, 10, 10, 0.5);
    }
    .stButton>button:hover, .stFormSubmitButton>button:hover {
        background: #cc3300 !important;       /* Darker red on hover */
        color: #ffffff !important;
    }
    .stTextInput>div>div>input, .stTextArea>div>textarea {
        background-color: #2b1a1a !important; /* Dark maroon */
        color: #ffece0 !important;
        border-radius: 6px !important;
        border: 1.5px solid #cc3300 !important;  /* Dark red border */
    }
    .stTabs [data-baseweb="tab-list"] {
        background: #2e1d1d;
        border-radius: 8px 8px 0 0;
    }
    .stTabs [data-baseweb="tab"] {
        font-weight: 600;
        color: #ffd1a4;                       /* Pale orange text */
    }
    .stTabs [aria-selected="true"] {
        background: #cc3300 !important;       /* Dark red selected tab */
        color: #ffffff !important;
        border-radius: 8px 8px 0 0;
    }
    .stAlert {
        border-radius: 8px !important;
        background: #2b1a1a !important;       /* Dark maroon */
        color: #ffece0 !important;
    }
    .stDataFrame {
        background: #2e1d1d !important;       /* Very dark maroon */
        border-radius: 10px !important;
        color: #ffece0 !important;
    }
    .resolve-card {
        background: #2b1a1a;
        border-radius: 14px;
        box-shadow: 0 2px 12px 0 rgba(44, 10, 10, 0.5);
        padding: 2rem 2rem 1.5rem 2rem;
        margin-bottom: 2rem;
        color: #ffece0;
    }
    .resolve-card h3 {
        color: #ffb380;                       /* Soft peach */
    }
    .resolve-card p {
        color: #ffd1a4;                       /* Pale orange */
    }
    .resolve-success {
        background: #442222;                  /* Dark burgundy */
        border-radius: 12px;
        padding: 2rem 2rem 1.5rem 2rem;
        text-align: center;
        margin-bottom: 2rem;
        border: 1.5px solid #ff4500;           /* Bright orange border */
        color: #ffece0;
    }
    .resolve-success span {
        color: #ffb380;                       /* Soft peach */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ─── HEADER ─────────────────────────────────────────────────────────────────────

st.markdown(
    """
    <div class="resolve-header">
        <h1>ResolveHub</h1>
        <p>Your friendly help desk for developer interns and tech leads.<br>
        <span style="font-size:1.5rem;">🤝</span></p>
    </div>
    """,
    unsafe_allow_html=True
)

# ─── FUNCTION TO HANDLE RERUN COMPATIBILITY ─────────────────────────────────────

def safe_rerun():
    """Handle rerun compatibility across Streamlit versions"""
    try:
        st.rerun()
    except AttributeError:
        try:
            st.experimental_rerun()
        except AttributeError:
            # If neither works, we'll just refresh the page state
            st.session_state._rerun_requested = True

# ─── INITIALIZE SESSION STATE ──────────────────────────────────────────────────

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.user = None

# ─── LOGIN / REGISTER UI (ONLY IF NOT LOGGED IN) ────────────────────────────────

if not st.session_state.logged_in:
    auth_mode = st.radio("Choose an option", ["Login", "Register"], horizontal=True)
    users_df = load_users()

    if auth_mode == "Register":
        st.subheader("📝 Register for ResolveHub")
        with st.form("register_form", clear_on_submit=True):
            reg_email = st.text_input("Email", key="reg_email")
            reg_password = st.text_input("Password", type="password", key="reg_password")
            reg_role = st.selectbox("Register as", ["Developer Intern", "Tech Lead"], key="reg_role")
            reg_submit = st.form_submit_button("Register")

        if reg_submit:
            if reg_email and reg_password and reg_role:
                if not reg_email.strip().endswith("@gmail.com"):
                    st.warning("Please enter a valid Gmail address ending with @gmail.com.")
                else:
                    success = save_user(reg_email, reg_password, reg_role)
                    if success:
                        st.success("✅ Registered successfully! You can now switch to Login.")
                    else:
                        st.error("⚠️ Email already registered.")
            else:
                st.warning("Please fill in all fields.")

        st.stop()

    else:  # Login path
        st.subheader("🔐 Login to ResolveHub")
        with st.form("login_form", clear_on_submit=True):
            username = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            login_submit = st.form_submit_button("Login")

        if login_submit:
            username_clean = username.strip()
            password_clean = password.strip()
            if not username_clean.endswith("@gmail.com"):
                st.warning("Please enter a valid Gmail address ending with @gmail.com.")
            else:
                match = users_df[
                    (users_df["email"].str.strip() == username_clean) &
                    (users_df["password"].astype(str).str.strip() == password_clean)
                ]
                if not match.empty:
                    st.session_state.logged_in = True
                    st.session_state.role = match.iloc[0]["role"]
                    st.session_state.user = username_clean
                    safe_rerun()
                else:
                    st.error("Invalid email or password.")
                    st.stop()

        st.stop()

# ─── AFTER LOGIN: SIDEBAR & LOGOUT ───────────────────────────────────────────────

role = st.session_state.role
st.sidebar.markdown("---")
st.sidebar.write(f"Logged in as: {st.session_state.user} ({role})")
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.user = None
    st.session_state.issue_submitted = False  # Reset form state if present
    safe_rerun()
st.sidebar.markdown("---")

# ─── HELPER TO LOAD + NORMALIZE issues.csv ───────────────────────────────────────

def load_and_normalize_issues(path=ISSUES_CSV):
    """
    - Reads the CSV at `path` (if it exists).
    - Ensures columns: ['ID','Name','Email','College','Title','Description',
      'Urgency','Status','Timestamp','ResolvedBy','Response']
    - Renames old columns 'Issue' -> 'Title', 'TechLeadResponse' -> 'Response' if present.
    - Fills missing final columns with empty strings and drops extras.
    """
    final_cols = [
        "ID", "Name", "Email", "College", "Title", "Description",
        "Urgency", "Status", "Timestamp", "ResolvedBy", "Response"
    ]

    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        return pd.DataFrame(columns=final_cols)

    # Rename legacy columns if present
    if "Issue" in df.columns and "Title" not in df.columns:
        df = df.rename(columns={"Issue": "Title"})
    if "TechLeadResponse" in df.columns and "Response" not in df.columns:
        df = df.rename(columns={"TechLeadResponse": "Response"})

    # Ensure all final_cols exist
    for c in final_cols:
        if c not in df.columns:
            df[c] = ""

    # Reorder and drop extras
    df = df[final_cols]
    return df

# ─── DEVELOPER INTERN SECTION ───────────────────────────────────────────────────

if role == "Developer Intern":
    st.markdown(
        "<div class='resolve-card'>"
        "<h3 style='color:#ffece0;margin-bottom:0.5rem;'>Raise a New Issue 🚀</h3>"
        "<div style='color:#ffd1a4;font-size:1.1rem;'>Fill out the form below and our tech leads will help you soon!</div>"
        "</div>",
        unsafe_allow_html=True
    )

    if "issue_submitted" not in st.session_state:
        st.session_state.issue_submitted = False

    if not st.session_state.issue_submitted:
        with st.form("issue_form", clear_on_submit=True):
            name        = st.text_input("Your Name", key="int_name")
            email       = st.text_input("Your Email (must be @gmail.com)", key="int_email")
            college     = st.text_input("Your College", key="int_college")
            title       = st.text_input("Issue Title", key="int_title")
            description = st.text_area("Describe the issue", key="int_description")
            urgency     = st.selectbox("Urgency", ["Low", "Medium", "High"], key="int_urgency")
            submitted   = st.form_submit_button("Submit Issue")

        if submitted:
            if not (name and email and college and title and description and urgency):
                st.warning("Please fill in all the fields to proceed.")
            elif not email.strip().endswith("@gmail.com"):
                st.warning("Please enter a valid Gmail address ending with @gmail.com.")
            else:
                new_issue = {
                    "ID":         datetime.now().strftime("%Y%m%d%H%M%S%f"),
                    "Name":       name,
                    "Email":      email,
                    "College":    college,
                    "Title":      title,
                    "Description":description,
                    "Urgency":    urgency,
                    "Status":     "Open",
                    "Timestamp":  datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "ResolvedBy": "",
                    "Response":   ""
                }

                df_existing = load_and_normalize_issues(ISSUES_CSV)
                df_existing = pd.concat([df_existing, pd.DataFrame([new_issue])], ignore_index=True)
                df_existing.to_csv(ISSUES_CSV, index=False)
                st.session_state.issue_submitted = True
                safe_rerun()
    else:
        st.markdown(
            "<div class='resolve-success'>"
            "<span style='font-size:2.5rem;'>🎉</span><br>"
            "<span style='color:#ffb380;font-size:1.3rem;font-weight:600;'>Issue submitted successfully!</span><br>"
            "<span style='color:#ffd1a4;'>Our tech leads will get back to you soon.</span>"
            "</div>",
            unsafe_allow_html=True
        )
        st.write("")
        if st.button("Any more queries?"):
            st.session_state.issue_submitted = False
            safe_rerun()

# ─── TECH LEAD SECTION ───────────────────────────────────────────────────────────

elif role == "Tech Lead":
    st.markdown(
        "<div class='resolve-card'>"
        "<h3 style='color:#ffece0;margin-bottom:0.5rem;'>🛠️ Tech Lead Panel</h3>"
        "<div style='color:#ffd1a4;font-size:1.1rem;'>View, respond, and resolve issues raised by developer interns.</div>"
        "</div>",
        unsafe_allow_html=True
    )
    techlead_email = st.text_input("Enter your email to resolve issues:", key="tl_email")

    # Load + normalize issues.csv
    df = load_and_normalize_issues(ISSUES_CSV)

    if df.empty:
        st.info("No issues have been reported yet.")
    else:
        tab1, tab2 = st.tabs(["🕒 Open Issues", "✅ Resolved Issues"])

        with tab1:
            st.subheader("🕒 Open Issues")
            open_issues = df[df["Status"] == "Open"].reset_index(drop=True)

            if open_issues.empty:
                st.info("No open issues.")
            else:
                for i, row in open_issues.iterrows():
                    with st.expander(f"{row['Title']} (by {row['Name']})", expanded=False):
                        st.markdown(f"**Title:** {row['Title']}")
                        st.markdown(f"**Description:** {row['Description']}")
                        st.markdown(f"**Raised by:** {row['Name']} ({row['Email']})")
                        st.markdown(f"**College:** {row['College']}")
                        st.markdown(f"**Urgency:** {row['Urgency']}")
                        st.markdown(f"**Timestamp:** {row['Timestamp']}")

                        response_key = f"response_{row['ID']}"
                        response_text = st.text_area("Response:", key=response_key)

                        button_key = f"resolve_{row['ID']}"
                        if st.button("Mark as Resolved ✔️", key=button_key):
                            if not techlead_email:
                                st.warning("Please enter your email before resolving issues.")
                            else:
                                df.loc[df["ID"] == row["ID"], "Status"]     = "Resolved"
                                df.loc[df["ID"] == row["ID"], "ResolvedBy"] = techlead_email
                                df.loc[df["ID"] == row["ID"], "Response"]   = response_text
                                df.to_csv(ISSUES_CSV, index=False)
                                st.success(f"Issue marked as resolved by {techlead_email}")
                                safe_rerun()

        with tab2:
            st.subheader("✅ Resolved Issues")
            resolved_issues = df[df["Status"] == "Resolved"]

            if resolved_issues.empty:
                st.info("No resolved issues yet.")
            else:
                for i, row in resolved_issues.iterrows():
                    with st.expander(f"{row['Title']} (by {row['Name']})", expanded=False):
                        st.markdown(f"**Title:** {row['Title']}")
                        st.markdown(f"**Description:** {row['Description']}")
                        st.markdown(f"**Raised by:** {row['Name']} ({row['Email']})")
                        st.markdown(f"**College:** {row['College']}")
                        st.markdown(f"**Urgency:** {row['Urgency']}")
                        st.markdown(f"**Resolved By:** {row.get('ResolvedBy', 'Unknown')}")
                        st.markdown(f"**Response:** {row.get('Response', 'No response')}")
                        st.markdown(f"**Timestamp:** {row['Timestamp']}")
                        st.markdown("---")

        # ─── All Reported Issues Table ────────────────────────────────────────
        st.subheader("📋 All Reported Issues")
        st.dataframe(df)

        # ─── Issues Resolved per Tech Lead Chart ────────────────────────────
        st.subheader("👨‍💻 Issues Resolved per Tech Lead")
        resolved_df = df[df["Status"] == "Resolved"]

        if not resolved_df.empty and "ResolvedBy" in resolved_df.columns:
            resolved_count = (
                resolved_df
                .groupby("ResolvedBy")
                .size()
                .reset_index(name="Count")
                .sort_values("Count", ascending=False)
            )

            chart = (
                alt.Chart(resolved_count)
                   .mark_bar(size=30)
                   .encode(
                       x=alt.X("ResolvedBy:N", title="Tech Lead"),
                       y=alt.Y("Count:Q", title="Resolved Issues"),
                       tooltip=["ResolvedBy", "Count"]
                   )
                   .properties(width=600, height=400)
            )
            st.altair_chart(chart, use_container_width=True)
        else:
            st.info("No resolved issues have 'ResolvedBy' data yet.")

# ─── GLOBAL STATS (BOTTOM) ─────────────────────────────────────────────────────

st.header("📊 Issue Tracker Stats")
df_stats = load_and_normalize_issues(ISSUES_CSV)

if not df_stats.empty:
    total_issues    = len(df_stats)
    resolved_issues = len(df_stats[df_stats["Status"] == "Resolved"])
    open_issues     = len(df_stats[df_stats["Status"] == "Open"])

    col1, col2, col3 = st.columns(3)
    col1.metric("📌 Total Issues", total_issues)
    col2.metric("✅ Resolved Issues", resolved_issues)
    col3.metric("🕒 Open Issues", open_issues)
else:
    st.warning("No data available yet.")
