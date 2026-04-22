import streamlit as st
import pandas as pd
from connection import get_google_sheet

st.title("🏥 Facilities Management")

try:
    sheet = get_google_sheet()
    facilities_sheet = sheet.worksheet("Facilities")
    facilities_df = pd.DataFrame(facilities_sheet.get_all_records())

    with st.expander("Add New Facility"):
        name = st.text_input("Facility Name")
        township = st.text_input("Township")
        state = st.text_input("State")

        if st.button("Add Facility"):
            if name.strip() and township.strip() and state.strip():
                next_id = len(facilities_df) + 1
                facilities_sheet.append_row([next_id, name, township, state])
                st.success("Facility added!")
                st.rerun()
            else:
                st.error("All fields are required")

    st.subheader("Facilities List")
    st.dataframe(facilities_df, use_container_width=True)

except Exception as e:
    st.error(f"Connection Error: {e}")
  
