import streamlit as st
import pandas as pd
from connection import get_google_sheet # connection.py မှ လှမ်းခေါ်ခြင်း

st.title("Treatment")

# Connection ကို Centralized function မှတစ်ဆင့်ယူခြင်း
try:
    sheet = get_google_sheet()
    
    # Load patients
    patients_sheet = sheet.worksheet("Patients")
    patients_data = patients_sheet.get_all_records()
    patients_df = pd.DataFrame(patients_data)
    patients_df.columns = patients_df.columns.str.strip()

    # Load existing treatment data
    treatment_sheet = sheet.worksheet("Treatment")
    treatment_data = treatment_sheet.get_all_records()
    treatment_df = pd.DataFrame(treatment_data)

    if patients_df.empty:
        st.warning("No patients found. Please add patient first.")

    else:
        # Dropdown
        patient_dict = {f"{row['patient_id']} - {row['name']}": row['patient_id'] for _, row in patients_df.iterrows()}
        selected = st.selectbox("Select Patient", list(patient_dict.keys()))

        # Define patient_id
        patient_id = patient_dict[selected]

        # Inputs
        art = st.selectbox("ART Status", ["On ART", "Not on ART"])
        pregnancy = st.selectbox("Pregnancy Status", ["Yes", "No"])

        # Save Button
        if st.button("Save Treatment", key="save_treatment_btn"):
            
            # Get next treatment_id (ပိုမိုသေချာစေရန် လက်ရှိ Table ရဲ့ အကြီးဆုံး ID ကိုယူခြင်း)
            next_treatment_id = len(treatment_df) + 1

            new_row = [
                next_treatment_id,
                patient_id,
                art,
                pregnancy
            ]

            treatment_sheet.append_row(new_row)

            st.success("✅ Treatment recorded successfully")
            
            # Data သစ်သွင်းပြီးရင် ချက်ချင်း Update ဖြစ်အောင် Rerun လုပ်ပေးခြင်း
            st.rerun()

except Exception as e:
    st.error(f"Error connecting to Google Sheets: {e}")
  
