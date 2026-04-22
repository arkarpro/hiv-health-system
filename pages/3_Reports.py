import streamlit as st
import pandas as pd
from connection import get_google_sheet

st.title("📊 Dashboard")

try:
    sheet = get_google_sheet()

    # Load data from Google Sheets
    testing = pd.DataFrame(sheet.worksheet("HIV_Testing").get_all_records())
    treatment = pd.DataFrame(sheet.worksheet("Treatment").get_all_records())

    # Whitespace cleanup
    if not testing.empty: testing.columns = testing.columns.str.strip()
    if not treatment.empty: treatment.columns = treatment.columns.str.strip()

    # Layout using columns
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Tested", len(testing))
    
    with col2:
        if not testing.empty and "result" in testing.columns:
            st.metric("Positive Cases", len(testing[testing["result"] == "Positive"]))
    
    with col3:
        if not treatment.empty and "ART_status" in treatment.columns:
            st.metric("On ART", len(treatment[treatment["ART_status"] == "On ART"]))

    st.divider()

    # Charts
    c1, c2 = st.columns(2)
    with c1:
        if not testing.empty and "result" in testing.columns:
            st.subheader("Testing Results")
            st.bar_chart(testing["result"].value_counts())

    with c2:
        if not treatment.empty and "ART_status" in treatment.columns:
            st.subheader("ART Status Distribution")
            st.bar_chart(treatment["ART_status"].value_counts())

except Exception as e:
    st.error(f"Error loading dashboard: {e}")
  
