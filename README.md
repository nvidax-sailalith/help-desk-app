# Help Desk Application

This is a help desk application built using Streamlit, designed to facilitate communication between developer interns and tech lead interns. Developer interns can submit their issues, and tech leads can view, respond to, and mark those issues as solved.

## Project Structure

```
help-desk-app
├── src
│   ├── app.py                  # Main entry point of the application
│   ├── components
│   │   ├── developer_form.py   # Form for developer interns to submit issues
│   │   ├── techlead_dashboard.py# Dashboard for tech leads to manage issues
│   │   └── issue_list.py       # Function to display the list of issues
│   ├── models
│   │   └── issue.py            # Issue model representing an issue
│   └── utils
│       └── storage.py          # Utility functions for data storage
├── requirements.txt             # Project dependencies
└── README.md                    # Project documentation
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd help-desk-app
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   streamlit run src/app.py
   ```

## Usage Guidelines

- Developer interns can fill out the form to submit their issues, providing their name, college, registered email, and a description of the issue.
- Tech lead interns can access the dashboard to view all submitted issues, respond to them, and mark them as solved.

## Features

- User-friendly interface for submitting and managing issues.
- Real-time updates for tech leads to respond to developer interns.
- Ability to track the status of issues (unsolved or solved).

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.