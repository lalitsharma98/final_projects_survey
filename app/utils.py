import streamlit as st
import pandas as pd
from datetime import datetime
import io
from firebase_setup import db

# -------------------------
# 🚀 App Setup
# -------------------------
st.set_page_config(page_title="Project Survey & Composite Score", layout="wide")
st.title("📊 Project Survey and Composite Score Viewer")

# -------------------------
# 🧭 Sidebar Navigation
# -------------------------
st.sidebar.title("Navigation")
option = st.sidebar.selectbox("Choose an option:", ["Fill Out Survey", "View Composite Scores"])

# Admin credentials
ADMIN_USERS = {"Jesse": "admin123", "Chetan": "admin456"}

# Projects & Assignments
projects = [
    "Anomaly Detection - Phase 1",
    "Model Validation - Phase 1",
    "Language Prioritization",
    "Automated WP Notes - Phase 1",
    "Data Extraction: MS Excel - Phase 1"
]

users_projects = {
    "Adrian": [1, 1, 0, 1, 0],
    "Chetan": [0, 0, 0, 0, 1],
    "Claudio": [1, 1, 0, 1, 0],
    "Danish": [0, 0, 0, 0, 1],
    "Gabi": [1, 1, 0, 1, 0],
    "Isaias": [1, 1, 0, 1, 0],
    "Jesse": [1, 1, 1, 1, 0],
    "Joel": [1, 1, 0, 1, 0],
    "Lalit": [0, 0, 0, 0, 1],
    "Laurie": [1, 1, 1, 1, 0],
    "Maricela": [1, 1, 0, 1, 0],
    "Mario": [1, 1, 0, 1, 0],
    "Paul": [1, 1, 0, 1, 0],
    "Vibhor": [1, 1, 0, 1, 0]
}

# -------------------------
# 📝 Fill Out Survey
# -------------------------
if option == "Fill Out Survey":
    selected_user = st.selectbox("Select User", list(users_projects.keys()))
    if selected_user:
        st.header(f"📝 Survey for {selected_user}")
        survey_data = []
        projects_list = users_projects[selected_user]

        for i, project_status in enumerate(projects_list):
            if project_status == 1:
                st.subheader(projects[i])
                usage = st.radio("Usage Status", ["Not Used", "Started Exploring", "Started Utilizing", "Regularly Utilizing/Reaping Benefit"], key=f"usage_{i}")
                feedback = st.radio("Feedback", ["Not Used", "No Issue", "Feature Request", "Design Issue", "Performance Issue", "Logical Issue"], key=f"feedback_{i}")
                usefulness = st.radio("Usefulness", ["Not Used", "Needs Improvement", "Somewhat Useful", "Very Useful"], key=f"usefulness_{i}")
                features = st.radio("Features Explored", ["Never", "Partial", "Fully"], key=f"features_{i}")
                frequency = st.radio("Frequency of Use", ["Never", "Rarely (once a month)", "Occasionally (a few times a month)", "Frequently (a few times a week)", "Almost Daily"], key=f"frequency_{i}")
                comments = st.text_area("Comments", key=f"comments_{i}")

                survey_data.append({
                    "User": selected_user,
                    "Project": projects[i],
                    "Usage Status": usage,
                    "Feedback": feedback,
                    "Usefulness": usefulness,
                    "Features Explored": features,
                    "Frequency of Use": frequency,
                    "Comments": comments,
                    "Month Year": datetime.now().strftime("%B %Y")
                })

        if st.button("Submit Survey"):
            for entry in survey_data:
                doc_id = f"{entry['Project']}_{entry['User']}_{entry['Month Year']}".replace(" ", "_")
                db.collection("survey_responses").document(doc_id).set(entry)
            st.success("✅ Survey submitted!")

# -------------------------
# 📈 View Composite Scores
# -------------------------
elif option == "View Composite Scores":
    try:
        docs = db.collection("survey_responses").stream()
        data = [doc.to_dict() for doc in docs]

        if data:
            df = pd.DataFrame(data)

            # Scoring maps
            usage_score_map = {
                "Not Used": 0,
                "Started Exploring": 2,
                "Started Utilizing": 5,
                "Regularly Utilizing/Reaping Benefit": 10
            }
            feedback_score_map = {
                "Not Used": 0,
                "No Issue": 2,
                "Feature Request": 5,
                "Design Issue": 8,
                "Performance Issue": 8,
                "Logical Issue": 10
            }
            usefulness_score_map = {
                "Not Used": 0,
                "Needs Improvement": 4,
                "Somewhat Useful": 6,
                "Very Useful": 10
            }
            features_score_map = {
                "Never": 0,
                "Partial": 5,
                "Fully": 10
            }
            frequency_score_map = {
                "Never": 0,
                "Rarely (once a month)": 2,
                "Occasionally (a few times a month)": 5,
                "Frequently (a few times a week)": 8,
                "Almost Daily": 10
            }

            # Apply scores
            df["Usage Score"] = df["Usage Status"].map(usage_score_map)
            df["Feedback Score"] = df["Feedback"].map(feedback_score_map)
            df["Usefulness Score"] = df["Usefulness"].map(usefulness_score_map)
            df["Features Score"] = df["Features Explored"].map(features_score_map)
            df["Frequency Score"] = df["Frequency of Use"].map(frequency_score_map)

            # Composite score
            max_score = 50
            df["Composite Score (%)"] = (
                df[["Usage Score", "Feedback Score", "Usefulness Score", "Features Score", "Frequency Score"]].sum(axis=1) / max_score
            ) * 100

            # Force score to 0 if all inputs are unused
            df.loc[
                (df["Usage Status"] == "Not Used") &
                (df["Feedback"] == "Not Used") &
                (df["Usefulness"] == "Not Used") &
                (df["Features Explored"] == "Never") &
                (df["Frequency of Use"] == "Never"),
                "Composite Score (%)"
            ] = 0

            df["Composite Score (%)"] = df["Composite Score (%)"].round(2)

            composite_scores = df.groupby(["User", "Month Year"])["Composite Score (%)"].mean().reset_index()
            st.subheader("📊 Month-Wise Composite Scores")
            st.dataframe(composite_scores, use_container_width=True)
        else:
            st.info("No survey data available.")
    except Exception as e:
        st.error(f"Error loading composite scores: {e}")

# -------------------------
# 🔐 Admin Panel
# -------------------------
selected_user = st.sidebar.selectbox("Admin Access (Optional)", list(users_projects.keys()), key="admin_select")
if selected_user in ADMIN_USERS:
    st.sidebar.markdown("### 🔐 Admin Panel")
    admin_password = st.sidebar.text_input("Enter Admin Password", type="password", key="admin_password")
    if ADMIN_USERS[selected_user] == admin_password:
        docs = db.collection("survey_responses").stream()
        data = []

        for doc in docs:
            entry = doc.to_dict()
            row = {
                "Key1": doc.id,
                "User": entry.get("User", ""),
                "Project": entry.get("Project", ""),
                "Usage Status": entry.get("Usage Status", ""),
                "Feedback": entry.get("Feedback", ""),
                "Usefulness": entry.get("Usefulness", ""),
                "Features Explored": entry.get("Features Explored", ""),
                "Frequency of Use": entry.get("Frequency of Use", ""),
                "Comments": entry.get("Comments", ""),
                "Month Year": entry.get("Month Year", "")
            }
            data.append(row)

        if data:
            df = pd.DataFrame(data)
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                df.to_excel(writer, index=False, sheet_name="Survey Data")
            output.seek(0)

            st.sidebar.download_button(
                label="📥 Download Survey Data",
                data=output,
                file_name="survey_results.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.sidebar.error("No survey data found.")
    elif admin_password:
        st.sidebar.error("❌ Invalid admin password")
