import streamlit as st
import pandas as pd

def show_composite_score_trends(df):
    st.subheader("📈 Composite Score Trend Over Time")

    df["Month Year Parsed"] = pd.to_datetime(df["Month Year"], format="%B %Y")
    selected_users = st.multiselect("Select Users to Visualize", df["User"].unique(), default=df["User"].unique())
    filtered_df = df[df["User"].isin(selected_users)]

    trend_df = (
        filtered_df
        .groupby(["User", "Month Year Parsed"])["Composite Score (%)"]
        .mean()
        .reset_index()
        .sort_values(by="Month Year Parsed")
    )

    pivot_df = trend_df.pivot(index="Month Year Parsed", columns="User", values="Composite Score (%)")
    st.line_chart(pivot_df)

    st.subheader("📊 Average Composite Score Per Month")
    monthly_avg = (
        filtered_df.groupby("Month Year Parsed")["Composite Score (%)"]
        .mean()
        .reset_index()
        .sort_values(by="Month Year Parsed")
    )
    st.bar_chart(data=monthly_avg, x="Month Year Parsed", y="Composite Score (%)")
