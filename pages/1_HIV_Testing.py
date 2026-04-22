import streamlit as st
import pandas as pd
from connection import get_google_sheet

st.title("🔬 HIV Testing")

try:
    # Google Sheets ချိတ်ဆက်ခြင်း
    sheet = get_google_sheet()

    # လူနာစာရင်း (Patients) ကိုယူခြင်း
    patients_sheet = sheet.worksheet("Patients")
    patients_df = pd.DataFrame(patients_sheet.get_all_records())
    patients_df.columns = patients_df.columns.str.strip()

    # ဆေးစစ်ချက်မှတ်တမ်း (HIV_Testing) ကိုယူခြင်း
    testing_sheet = sheet.worksheet("HIV_Testing")
    testing_df = pd.DataFrame(testing_sheet.get_all_records())

    if patients_df.empty:
        st.warning("⚠️ No patients found. Please add a patient in the Patient Management page first.")
    else:
        # User Interface - Form အသုံးပြုခြင်း
        with st.form("testing_form"):
            st.subheader("Record New Test Result")
            
            # လူနာရွေးချယ်ရန် Dropdown
            patient_dict = {f"{row['patient_id']} - {row['name']}": row['patient_id'] for _, row in patients_df.iterrows()}
            selected = st.selectbox("Select Patient", list(patient_dict.keys()))
            
            # စစ်ဆေးသည့်ရက်စွဲနှင့် အဖြေ
            test_date = st.date_input("Test Date")
            result = st.selectbox("Result", ["Negative", "Positive"])
            
            submit = st.form_submit_button("Save Test Result")

            if submit:
                patient_id = patient_dict[selected]
                
                # ID ပေးပုံကို စနစ်တကျ ပြင်ဆင်ခြင်း
                next_test_id = len(testing_df) + 1

                new_row = [
                    next_test_id,
                    patient_id,
                    str(test_date),
                    result
                ]

                testing_sheet.append_row(new_row)
                st.success(f"✅ Test result for {selected} saved successfully!")
                
                # အဖြေ Positive ဖြစ်လျှင် သတိပေးခြင်း
                if result == "Positive":
                    st.warning("🚨 Important: Patient is HIV Positive. Please proceed to the Treatment Page.")
                
                st.rerun()

    # လက်ရှိစစ်ဆေးပြီးသမျှ စာရင်းကိုပြသရန်
    st.divider()
    st.subheader("Testing History")
    if not testing_df.empty:
        st.dataframe(testing_df, use_container_width=True)
    else:
        st.info("No testing records found.")

except Exception as e:
    st.error(f"Error connecting to database: {e}")
  
