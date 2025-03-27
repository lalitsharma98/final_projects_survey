# import streamlit as st
# import pandas as pd
# from datetime import datetime
# import io
# from app.firebase_setup import db

# # -------------------------
# # 🔍 Composite Score Viewer
# # -------------------------
# with st.expander("🔍 View Composite Scores"):
#     try:
#         docs = db.collection("survey_responses").stream()
#         data = [doc.to_dict() for doc in docs]

#         if data:
#             df = pd.DataFrame(data)

#             # Score mappings
#             usage_score_map = {
#                 "Not Used": 0,
#                 "Started Exploring": 2,
#                 "Started Utilizing": 5,
#                 "Regularly Utilizing/Reaping Benefit": 10
#             }
#             feedback_score_map = {
#                 "Not Used": 0,
#                 "No Issue": 2,
#                 "Feature Request": 5,
#                 "Design Issue": 8,
#                 "Performance Issue": 8,
#                 "Logical Issue": 10
#             }
#             features_score_map = {
#                 "Never": 0,
#                 "Partial": 5,
#                 "Fully": 10
#             }
#             frequency_score_map = {
#                 "Never": 0,
#                 "Rarely (once a month)": 2,
#                 "Occasionally (a few times a month)": 5,
#                 "Frequently (a few times a week)": 8,
#                 "Almost Daily": 10
#             }

#             max_score = 40  # Total possible score

#             # Score columns
#             df["Usage Score"] = df["Usage Status"].map(usage_score_map)
#             df["Feedback Score"] = df["Feedback"].map(feedback_score_map)
#             df["Features Score"] = df["Features Explored"].map(features_score_map)
#             df["Frequency Score"] = df["Frequency of Use"].map(frequency_score_map)

#             # Composite score
#             df["Composite Score (%)"] = (
#                 df[["Usage Score", "Feedback Score", "Features Score", "Frequency Score"]].sum(axis=1) / max_score
#             ) * 100

#             composite_scores = df.groupby(["User", "Month Year"])["Composite Score (%)"].mean().reset_index()

#             st.subheader("📊 Month-Wise Composite Scores")
#             st.dataframe(composite_scores)
#         else:
#             st.info("No survey data available.")
#     except Exception as e:
#         st.error(f"Failed to load data from Firebase: {e}")


# # -------------------------
# # 🎯 Main Survey Interface
# # -------------------------
# st.title("Project Survey")

# projects = [
#     "Anomaly Detection - Phase 1", "Model Validation - Phase 1", "Language Prioritization",
#     "Automated WP Notes - Phase 1", "Data Extraction: MS Excel - Phase 1"
# ]

# users_projects = {
#     "Adrian": [1, 1, "", 1, ""],
#     "Chetan": ["", "", "", "", 1],
#     "Claudio": [1, 1, "", 1, ""],
#     "Danish": ["", "", "", "", 1],
#     "Gabi": [1, 1, "", 1, ""],
#     "Isaias": [1, 1, "", 1, ""],
#     "Jesse": [1, 1, 1, 1, ""],
#     "Joel": [1, 1, "", 1, ""],
#     "Lalit": ["", "", "", "", 1],
#     "Laurie": [1, 1, 1, 1, ""],
#     "Maricela": [1, 1, "", 1, ""],
#     "Mario": [1, 1, "", 1, ""],
#     "Paul": [1, 1, "", 1, ""],
#     "Vibhor": [1, 1, "", 1, ""]
# }

# ADMIN_USERS = {"Jesse": "admin123", "Chetan": "admin456"}

# selected_user = st.selectbox("Select User", list(users_projects.keys()))

# if selected_user:
#     st.header(f"Projects for {selected_user}")
#     survey_data = []
#     projects_list = users_projects[selected_user]
#     for i, project_status in enumerate(projects_list):
#         if project_status == 1:
#             st.subheader(projects[i])
#             usage = st.radio(
#                 f"Usage Status for {projects[i]}",
#                 ["Not Used", "Started Exploring", "Started Utilizing", "Regularly Utilizing/Reaping Benefit"],
#                 key=f"usage_{selected_user}_{projects[i]}"
#             )
#             feedback = st.radio(
#                 f"Feedback for {projects[i]}",
#                 ["Not Used", "No Issue", "Feature Request", "Design Issue", "Performance Issue", "Logical Issue"],
#                 key=f"feedback_{selected_user}_{projects[i]}"
#             )
#             features = st.radio(
#                 f"Features Explored for {projects[i]}",
#                 ["Never", "Partial", "Fully"],
#                 key=f"features_{selected_user}_{projects[i]}"
#             )
#             frequency = st.radio(
#                 f"Frequency of Use for {projects[i]}",
#                 ["Never", "Rarely (once a month)", "Occasionally (a few times a month)", "Frequently (a few times a week)", "Almost Daily"],
#                 key=f"frequency_{selected_user}_{projects[i]}"
#             )
#             comments = st.text_area(f"Comments for {projects[i]}", key=f"comments_{selected_user}_{projects[i]}")
#             survey_data.append({
#                 "User": selected_user,
#                 "Project": projects[i],
#                 "Usage Status": usage,
#                 "Feedback": feedback,
#                 "Features Explored": features,
#                 "Frequency of Use": frequency,
#                 "Comments": comments,
#                 "Month Year": datetime.now().strftime("%B %Y")
#             })

#     if st.button("Submit Survey"):
#         for entry in survey_data:
#             doc_id = f"{entry['Project']}_{entry['User']}_{entry['Month Year']}".replace(" ", "_")
#             db.collection("survey_responses").document(doc_id).set(entry)
#         st.success("Survey submitted successfully!")


# # -------------------------
# # 🔐 Admin Panel
# # -------------------------
# if selected_user in ADMIN_USERS:
#     st.sidebar.header("Admin Panel")
#     admin_password = st.sidebar.text_input("Enter Password", type="password")

#     if st.sidebar.button("Download Survey Data"):
#         if ADMIN_USERS.get(selected_user) == admin_password:
#             docs = db.collection("survey_responses").stream()
#             data = []

#             for doc in docs:
#                 entry = doc.to_dict()
#                 row = {
#                     "Key1": doc.id,
#                     "User": entry.get("User", ""),
#                     "Project": entry.get("Project", ""),
#                     "Usage Status": entry.get("Usage Status", ""),
#                     "Feedback": entry.get("Feedback", ""),
#                     "Features Explored": entry.get("Features Explored", ""),
#                     "Frequency of Use": entry.get("Frequency of Use", ""),
#                     "Comments": entry.get("Comments", ""),
#                     "Month Year": entry.get("Month Year", "")
#                 }
#                 data.append(row)

#             if data:
#                 df = pd.DataFrame(data)
#                 output = io.BytesIO()
#                 with pd.ExcelWriter(output, engine='openpyxl') as writer:
#                     df.to_excel(writer, index=False, sheet_name="Survey Data")
#                 output.seek(0)

#                 st.sidebar.download_button(
#                     label="📥 Download Survey Data",
#                     data=output,
#                     file_name="survey_results_formatted.xlsx",
#                     mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#                 )
#             else:
#                 st.sidebar.error("No survey data found.")
#         else:
#             st.sidebar.error("Invalid admin credentials!")

import streamlit as st
import pandas as pd
from datetime import datetime
import os

# File path for survey results
file_path = "survey_results.xlsx"

# Project List
projects = ["Anomaly Detection - Phase 1", "Model Validation - Phase 1", "Language Prioritization", 
            "Automated WP Notes - Phase 1", "Data Extraction: MS Excel - Phase 1"]

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

# Scoring Mappings
usage_score_map = {"Not Used": 0, "Started Exploring": 2, "Started Utilizing": 5, "Regularly Utilizing/Reaping Benefit": 10}
feedback_score_map = {
    "Not Used": 0, "No Issue": 2, "Feature Request": 5, "Design Issue": 8, 
    "Performance Issue": 8, "Logical Issue": 10
}
features_score_map = {"Never": 0, "Partial": 5, "Fully": 10}
frequency_score_map = {
    "Never": 0, "Rarely (once a month)": 2, "Occasionally (a few times a month)": 5, 
    "Frequently (a few times a week)": 8, "Almost Daily": 10
}
usefulness_score_map = {
    "Not Used": 0, "Not Useful": 2, "Needs Improvement": 4, 
    "Somewhat Useful": 6, "Very Useful": 8, "Exceptionally Useful": 10
}

# Maximum possible score
max_score = 10 + 10 + 10 + 10 + 10  # Sum of the highest values from each mapping

# Function to calculate composite score
def calculate_composite_score(df):
    df["Usage Score"] = df["Usage Status"].map(usage_score_map)
    df["Feedback Score"] = df["Feedback"].map(feedback_score_map)
    df["Features Score"] = df["Features Explored"].map(features_score_map)
    df["Frequency Score"] = df["Frequency of Use"].map(frequency_score_map)
    df["Usefulness Score"] = df["Usefulness"].map(usefulness_score_map)
    
    # Calculate composite score as a percentage
    df["Composite Score (%)"] = (
        df[["Usage Score", "Feedback Score", "Features Score", "Frequency Score", "Usefulness Score"]].sum(axis=1) 
        / max_score
    ) * 100
    
    # Round to 2 decimal places
    df["Composite Score (%)"] = df["Composite Score (%)"].round(2)
    
    # Group by User and Month Year to calculate average composite score
    user_scores = df.groupby(["User", "Month Year"])["Composite Score (%)"].mean().reset_index()
    return user_scores

# Streamlit App
st.title("Project Survey and Composite Score Viewer")

# Sidebar for navigation
st.sidebar.title("Navigation")
option = st.sidebar.selectbox("Choose an option:", ["View Composite Scores", "Fill Out Survey"])

# Option 1: View Composite Scores
if option == "View Composite Scores":
    if os.path.exists(file_path):
        # Read the survey data
        df = pd.read_excel(file_path)
        
        if st.button("View Composite Scores"):
            composite_scores = calculate_composite_score(df)
            st.subheader("Month-Wise Composite Scores")
            st.dataframe(composite_scores)
    else:
        st.error("Survey data file not found.")

# Option 2: Fill Out Survey
elif option == "Fill Out Survey":
    selected_user = st.selectbox("Select User", list(users_projects.keys()))

    if selected_user:
        st.header(f"Projects for {selected_user}")
        survey_data = []
        projects_list = users_projects[selected_user]
        for i, project_status in enumerate(projects_list):
            if project_status == 1:
                st.subheader(projects[i])
                usage = st.radio(f"Usage Status for {projects[i]}", ["Not Used", "Started Exploring", "Started Utilizing", "Regularly Utilizing/Reaping Benefit"], key=f"usage_{selected_user}_{projects[i]}")
                feedback = st.radio(f"Feedback for {projects[i]}", ["Not Used", "No Issue", "Feature Request", "Design Issue", "Performance Issue", "Logical Issue"], key=f"feedback_{selected_user}_{projects[i]}")
                features = st.radio(f"Features Explored for {projects[i]}", ["Never", "Partial", "Fully"], key=f"features_{selected_user}_{projects[i]}")
                frequency = st.radio(f"Frequency of Use for {projects[i]}", ["Never", "Rarely (once a month)", "Occasionally (a few times a month)", "Frequently (a few times a week)", "Almost Daily"], key=f"frequency_{selected_user}_{projects[i]}")
                usefulness = st.radio(f"Usefulness for {projects[i]}", ["Not Used", "Not Useful", "Needs Improvement", "Somewhat Useful", "Very Useful", "Exceptionally Useful"], key=f"usefulness_{selected_user}_{projects[i]}")
                comments = st.text_area(f"Comments for {projects[i]}", key=f"comments_{selected_user}_{projects[i]}")
                survey_data.append([selected_user, projects[i], usage, feedback, features, frequency, usefulness, comments])

        if st.button("Submit Survey"):
            # Create a DataFrame from the survey data
            df = pd.DataFrame(survey_data, columns=["User", "Project", "Usage Status", "Feedback", "Features Explored", "Frequency of Use", "Usefulness", "Comments"])
            df["Month Year"] = datetime.now().strftime("%B %Y")

            if os.path.exists(file_path):
                # Load existing data
                existing_df = pd.read_excel(file_path)

                for i, row in df.iterrows():
                    condition = (
                        (existing_df["User"] == row["User"]) &
                        (existing_df["Project"] == row["Project"]) &
                        (existing_df["Month Year"] == row["Month Year"])
                    )
                    if condition.any():
                        # Update the existing row
                        existing_df.loc[condition, ["Usage Status", "Feedback", "Features Explored", "Frequency of Use", "Usefulness", "Comments"]] = row[["Usage Status", "Feedback", "Features Explored", "Frequency of Use", "Usefulness", "Comments"]].values
                    else:
                        # Append the new row
                        existing_df = pd.concat([existing_df, pd.DataFrame([row])], ignore_index=True)

                # Save the updated DataFrame
                existing_df.to_excel(file_path, index=False)
            else:
                # Save new data
                df.to_excel(file_path, index=False)

            st.success("Survey submitted successfully!")
