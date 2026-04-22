import streamlit as st
import pandas as pd
from connection import get_google_sheet

st.title("👥 Patient Management")

try:
    sheet_file = get_google_sheet()
    patients_sheet = sheet_file.worksheet("Patients")
    
    # Load and clean data
    data = patients_sheet.get_all_records()
    existing_data = pd.DataFrame(data)
    existing_data.columns = existing_data.columns.str.strip()

    # Registration Form
    with st.form("patient_form"):
        name = st.text_input("Name")
        sex = st.selectbox("Sex", ["Male", "Female", "Other"])
        age = st.number_input("Age", 0, 120)
        submit = st.form_submit_button("Save Patient")

        if submit:
            if name.strip() == "":
                st.error("Name is required")
            elif age <= 0:
                st.error("Please enter a valid age")
            else:
                new_row = [len(existing_data) + 1, name, sex, age]
                patients_sheet.append_row(new_row)
                st.success(f"✅ {name} added successfully")
                st.rerun()

    st.subheader("Current Patient List")
    st.dataframe(existing_data, use_container_width=True)

except Exception as e:
    st.error(f"Error: {e}")
  
