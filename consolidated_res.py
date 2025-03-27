# import streamlit as st
# import pandas as pd
# from datetime import datetime
# import os
# from io import BytesIO

# # Project List
# projects = [
#     "Anomaly Detection - Phase 1", "Model Validation - Phase 1", "Language Prioritization",
#     "Automated WP Notes - Phase 1", "Data Extraction: MS Excel - Phase 1"
# ]

# # Users and their project involvement matrix
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

# # Admin credentials
# ADMIN_USERS = {"Jesse": "admin123", "Chetan": "admin456"}

# # File path
# file_path = "survey_results.xlsx"

# # Streamlit app title
# st.title("Project Survey")

# # Button to view composite scores (placed at the top)
# with st.expander("🔍 View Composite Scores"):
#     if os.path.exists(file_path):
#         df = pd.read_excel(file_path)
        
#         usage_score_map = {"Not Used": 0, "Started Exploring": 2, "Started Utilizing": 5, "Regularly Utilizing/Reaping Benefit": 10}
#         feedback_score_map = {"Not Used": 0, "Needs Improvement": 5, "Somewhat Useful": 2, "Very Useful": 5}
#         features_score_map = {"Never": 0, "Partial": 5, "Fully": 10}
#         frequency_score_map = {"Never": 0, "Rarely (once a month)": 2, "Occasionally (a few times a month)": 5, "Frequently (a few times a week)": 8, "Almost Daily": 10}
        
#         max_score = 10 + 5 + 10 + 10  # Sum of highest scores from each category
        
#         df["Usage Score"] = df["Usage Status"].map(usage_score_map)
#         df["Feedback Score"] = df["Feedback"].map(feedback_score_map)
#         df["Features Score"] = df["Features Explored"].map(features_score_map)
#         df["Frequency Score"] = df["Frequency of Use"].map(frequency_score_map)
        
#         df["Composite Score (%)"] = (df[["Usage Score", "Feedback Score", "Features Score", "Frequency Score"]].sum(axis=1) / max_score) * 100
        
#         composite_scores = df.groupby(["User", "Month Year"])["Composite Score (%)"].mean().reset_index()
#         st.subheader("Month-Wise Composite Scores")
#         st.dataframe(composite_scores)
#     else:
#         st.error("Survey data file not found.")

# # User selection dropdown
# selected_user = st.selectbox("Select User", list(users_projects.keys()))

# # Survey form for selected user
# if selected_user:
#     st.header(f"Projects for {selected_user}")
#     survey_data = []
#     projects_list = users_projects[selected_user]
#     for i, project_status in enumerate(projects_list):
#         if project_status == 1:
#             st.subheader(projects[i])
#             usage = st.radio(f"Usage Status for {projects[i]}", ["Not Used", "Started Exploring", "Started Utilizing", "Regularly Utilizing/Reaping Benefit"], key=f"usage_{selected_user}_{projects[i]}")
#             feedback = st.radio(f"Feedback for {projects[i]}", ["Not Used","Needs Improvement", "Somewhat Useful", "Very Useful"], key=f"feedback_{selected_user}_{projects[i]}")
#             features = st.radio(f"Features Explored for {projects[i]}", ["Never", "Partial", "Fully"], key=f"features_{selected_user}_{projects[i]}")
#             frequency = st.radio(f"Frequency of Use for {projects[i]}", ["Never", "Rarely (once a month)", "Occasionally (a few times a month)", "Frequently (a few times a week)", "Almost Daily"], key=f"frequency_{selected_user}_{projects[i]}")
#             comments = st.text_area(f"Comments for {projects[i]}", key=f"comments_{selected_user}_{projects[i]}")
#             survey_data.append([selected_user, projects[i], usage, feedback, features, frequency, comments])

#     if st.button("Submit Survey"):
#         df = pd.DataFrame(survey_data, columns=["User", "Project", "Usage Status", "Feedback", "Features Explored", "Frequency of Use", "Comments"])
#         df["Month Year"] = datetime.now().strftime("%B %Y")

#         if os.path.exists(file_path):
#             existing_df = pd.read_excel(file_path)
#             existing_df = pd.concat([existing_df, df], ignore_index=True)
#         else:
#             existing_df = df
        
#         existing_df.to_excel(file_path, index=False)
#         st.success("Survey submitted successfully!")


# import streamlit as st
# import pandas as pd
# from datetime import datetime
# import os
# from io import BytesIO
# from firebase_setup import db

# # Firebase Admin SDK
# import firebase_admin
# from firebase_admin import credentials, firestore

# # Initialize Firebase app only once
# # if not firebase_admin._apps:
# #     cred = credentials.Certificate(r"C:\Users\sharma.15282\OneDrive - Teleperformance\What-Ifs\survey\firebase-key.json")
# #     firebase_admin.initialize_app(cred)
# print("We are here")
# # Firestore client
# db = firestore.client()

# # Project List
# projects = [
#     "Anomaly Detection - Phase 1", "Model Validation - Phase 1", "Language Prioritization",
#     "Automated WP Notes - Phase 1", "Data Extraction: MS Excel - Phase 1"
# ]

# print(f"our projects are:  {projects}")

# # Users and their project involvement matrix
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

# # Admin credentials
# ADMIN_USERS = {"Jesse": "admin123", "Chetan": "admin456"}

# # Local Excel file path (optional fallback or export)
# file_path = "survey_results.xlsx"

# print(f"file path is : {file_path}")

# # Streamlit app title
# st.title("📊 Project Survey")

# print(f"streamlit app starts here : ")

# # View Composite Scores from Local Excel (Optional)
# with st.expander("🔍 View Composite Scores"):
#     if os.path.exists(file_path):
#         df = pd.read_excel(file_path)

#         usage_score_map = {
#             "Not Used": 0,
#             "Started Exploring": 2,
#             "Started Utilizing": 5,
#             "Regularly Utilizing/Reaping Benefit": 10
#         }
#         feedback_score_map = {
#             "Not Used": 0,
#             "Needs Improvement": 5,
#             "Somewhat Useful": 2,
#             "Very Useful": 5
#         }
#         features_score_map = {"Never": 0, "Partial": 5, "Fully": 10}
#         frequency_score_map = {
#             "Never": 0,
#             "Rarely (once a month)": 2,
#             "Occasionally (a few times a month)": 5,
#             "Frequently (a few times a week)": 8,
#             "Almost Daily": 10
#         }

#         max_score = 10 + 5 + 10 + 10

#         df["Usage Score"] = df["Usage Status"].map(usage_score_map)
#         df["Feedback Score"] = df["Feedback"].map(feedback_score_map)
#         df["Features Score"] = df["Features Explored"].map(features_score_map)
#         df["Frequency Score"] = df["Frequency of Use"].map(frequency_score_map)

#         df["Composite Score (%)"] = (
#             df[["Usage Score", "Feedback Score", "Features Score", "Frequency Score"]].sum(axis=1) / max_score
#         ) * 100

#         composite_scores = df.groupby(["User", "Month Year"])["Composite Score (%)"].mean().reset_index()
#         st.subheader("Month-Wise Composite Scores")
#         st.dataframe(composite_scores)
#     else:
#         st.error("Survey data file not found.")

# # Dropdown to select user
# selected_user = st.selectbox("Select User", list(users_projects.keys()))

# # Survey Form
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
#                 ["Not Used", "Needs Improvement", "Somewhat Useful", "Very Useful"],
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
#             survey_data.append([
#                 selected_user, projects[i], usage, feedback, features, frequency, comments
#             ])

#     if st.button("Submit Survey"):
#         df = pd.DataFrame(survey_data, columns=[
#             "User", "Project", "Usage Status", "Feedback", "Features Explored", "Frequency of Use", "Comments"
#         ])
#         df["Month Year"] = datetime.now().strftime("%B %Y")

#         # 🔥 Push to Firestore
#         for _, row in df.iterrows():
#             survey_doc = {
#                 "user": row["User"],
#                 "project": row["Project"],
#                 "usage_status": row["Usage Status"],
#                 "feedback": row["Feedback"],
#                 "features_explored": row["Features Explored"],
#                 "frequency_of_use": row["Frequency of Use"],
#                 "comments": row["Comments"],
#                 "month_year": row["Month Year"],
#                 "timestamp": firestore.SERVER_TIMESTAMP
#             }
#             db.collection("surveyData").add(survey_doc)

#         # 💾 Optional Excel Backup
#         if os.path.exists(file_path):
#             existing_df = pd.read_excel(file_path)
#             existing_df = pd.concat([existing_df, df], ignore_index=True)
#         else:
#             existing_df = df
#         existing_df.to_excel(file_path, index=False)

#         st.success("✅ Survey submitted successfully!")

# # 🔍 Optional: Show all Firestore survey entries
# with st.expander("📋 View Submitted Surveys (from Firestore)"):
#     survey_docs = db.collection("surveyData").stream()
#     firestore_data = []
#     for doc in survey_docs:
#         firestore_data.append(doc.to_dict())
#     if firestore_data:
#         st.dataframe(pd.DataFrame(firestore_data))
#     else:
#         st.info("No survey data found in Firestore yet.")

print("1️⃣ Top of script loaded")

from projects_survey.app.firebase_setup import db
print("2️⃣ Firebase setup imported")

import streamlit as st
print("3️⃣ Streamlit imported")

st.title("🧪 Test")
print("4️⃣ Streamlit UI initialized")

st.write("✅ If you see this, app is alive!")
