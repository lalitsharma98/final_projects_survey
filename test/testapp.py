import streamlit as st
import pandas as pd
from datetime import datetime
import io
from projects_survey.app.firebase_setup import db

# 🔥 Firebase Firestore setup
from projects_survey.app.firebase_setup import db  # <- Import the Firestore client

# Project List
projects = [
    "Anomaly Detection - Phase 1", "Model Validation - Phase 1", "Language Prioritization",
    "Automated WP Notes - Phase 1", "Data Extraction: MS Excel - Phase 1"
]

# Users and their project involvement matrix
users_projects = {
    "Adrian": [1, 1, "", 1, ""],
    "Chetan": ["", "", "", "", 1],
    "Claudio": [1, 1, "", 1, ""],
    "Danish": ["", "", "", "", 1],
    "Gabi": [1, 1, "", 1, ""],
    "Isaias": [1, 1, "", 1, ""],
    "Jesse": [1, 1, 1, 1, ""],
    "Joel": [1, 1, "", 1, ""],
    "Lalit": ["", "", "", "", 1],
    "Laurie": [1, 1, 1, 1, ""],
    "Maricela": [1, 1, "", 1, ""],
    "Mario": [1, 1, "", 1, ""],
    "Paul": [1, 1, "", 1, ""],
    "Vibhor": [1, 1, "", 1, ""]
}

# Admin credentials
ADMIN_USERS = {"Jesse": "admin123", "Chetan": "admin456"}

# App title
st.title("Project Survey")

# User selection dropdown
selected_user = st.selectbox("Select User", list(users_projects.keys()))

# Survey form for selected user and their projects
if selected_user:
    st.header(f"Projects for {selected_user}")
    survey_data = []
    projects_list = users_projects[selected_user]
    for i, project_status in enumerate(projects_list):
        if project_status == 1:
            st.subheader(projects[i])
            usage = st.radio(f"Usage Status for {projects[i]}", ["Not Used", "Started Exploring", "Started Utilizing", "Regularly Utilizing/Reaping Benefit"], key=f"usage_{selected_user}_{projects[i]}")
            feedback = st.radio(f"Feedback for {projects[i]}", ["Not Used","Needs Improvement", "Somewhat Useful", "Very Useful"], key=f"feedback_{selected_user}_{projects[i]}")
            features = st.radio(f"Features Explored for {projects[i]}", ["Never", "Partial", "Fully"], key=f"features_{selected_user}_{projects[i]}")
            frequency = st.radio(f"Frequency of Use for {projects[i]}", ["Never", "Rarely (once a month)", "Occasionally (a few times a month)", "Frequently (a few times a week)", "Almost Daily"], key=f"frequency_{selected_user}_{projects[i]}")
            comments = st.text_area(f"Comments for {projects[i]}", key=f"comments_{selected_user}_{projects[i]}")
            survey_data.append({
                "User": selected_user,
                "Project": projects[i],
                "Usage Status": usage,
                "Feedback": feedback,
                "Features Explored": features,
                "Frequency of Use": frequency,
                "Comments": comments,
                "Month Year": datetime.now().strftime("%B %Y")
            })

    if st.button("Submit Survey"):
        for entry in survey_data:
            doc_id = f"{entry['User']}_{entry['Project']}_{entry['Month Year']}".replace(" ", "_")
            db.collection("survey_responses").document(doc_id).set(entry)
        st.success("Survey submitted successfully!")

# Admin Panel
if selected_user in ADMIN_USERS:
    st.sidebar.header("Admin Panel")
    admin_password = st.sidebar.text_input("Enter Password", type="password")

    if st.sidebar.button("Download Survey Data"):
        if ADMIN_USERS.get(selected_user) == admin_password:
            docs = db.collection("survey_responses").stream()
            data = [doc.to_dict() for doc in docs]

            if data:
                df = pd.DataFrame(data)
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False, sheet_name="Survey Data")
                output.seek(0)

                st.sidebar.download_button(
                    label="📥 Download Survey Data",
                    data=output,
                    file_name="survey_results_firestore.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.sidebar.error("No survey data found.")
        else:
            st.sidebar.error("Invalid admin credentials!")

# Reference to a collection called "testCollection"
# doc_ref = db.collection("testCollection").document("testDoc")

# # Set some test data
# doc_ref.set({
#     "name": "chetan sharma",
#     "email": "chetan@example.com",
#     "age": 27
# })
# print("Test document written!")
# Read the Test Document

# Get the document
# doc = db.collection("testCollection").document("testDoc").get()

# if doc.exists:
#     print("Document data:", doc.to_dict())
# else:
#     print("No such document found!")

