# UI ဖန်တီးရန် Streamlit နှင့် Data ဇယားများတွက်ချက်ရန် Pandas ကို ခေါ်ယူခြင်း
import streamlit as st
import pandas as pd
# ကျွန်တော်တို့ စနစ်တကျ ခွဲထုတ်ရေးသားထားတဲ့ Google Sheet ချိတ်ဆက်မယ့် Function ကို လှမ်းခေါ်ခြင်း
from connection import get_google_sheet

# စာမျက်နှာရဲ့ ခေါင်းစဉ်ကို သတ်မှတ်ခြင်း
st.title("💊 Treatment")

# အင်တာနက်ပြတ်တောက်ခြင်း သို့မဟုတ် Sheet ရှာမတွေ့ခြင်း စတဲ့ ပြဿနာများဖြစ်လာပါက 
# App ကြီး ပျက်မကျသွားစေရန် try-except block ဖြင့် ကာကွယ်ထားခြင်း
try:
    # Google Sheets နှင့် ချိတ်ဆက်ခြင်း (connection.py မှ Function ကို အသုံးပြုခြင်း)
    sheet = get_google_sheet()
    
    # လူနာစာရင်း (Patients) ကို Google Sheet ထဲမှ လှမ်းဖတ်ပြီး ဇယား (DataFrame) အဖြစ် ပြောင်းခြင်း
    patients_sheet = sheet.worksheet("Patients")
    patients_data = patients_sheet.get_all_records()
    patients_df = pd.DataFrame(patients_data)
    # ကော်လံနာမည်တွေမှာ မလိုအပ်တဲ့ Space (ကွက်လပ်) တွေ ပါနေရင် ရှင်းလင်းပေးခြင်း (Error မတက်အောင် ကာကွယ်ခြင်း)
    patients_df.columns = patients_df.columns.str.strip()

    # လက်ရှိ ထည့်သွင်းထားပြီးသော ကုသမှုမှတ်တမ်း (Treatment) များကို Google Sheet မှ လှမ်းဖတ်ခြင်း
    treatment_sheet = sheet.worksheet("Treatment")
    treatment_data = treatment_sheet.get_all_records()
    treatment_df = pd.DataFrame(treatment_data)

    # အကယ်၍ လူနာစာရင်းထဲမှာ Data လုံးဝမရှိသေးဘူးဆိုရင် User ကို သတိပေးချက်ပြသခြင်း
    if patients_df.empty:
        st.warning("⚠️ No patients found. Please add a patient first.")

    else:
        # လူနာရွေးချယ်ရန် Dropdown ဖန်တီးခြင်း
        # "1 - U Ba", "2 - Daw Hla" စသဖြင့် User မြင်ရလွယ်အောင် ID နှင့် Name ကို တွဲပေးခြင်း
        patient_dict = {f"{row['patient_id']} - {row['name']}": row['patient_id'] for _, row in patients_df.iterrows()}
        selected = st.selectbox("Select Patient", list(patient_dict.keys()))

        # User ရွေးချယ်လိုက်တဲ့ စာသားထဲကနေ Data သိမ်းရန်အတွက် အမှန်တကယ် လိုအပ်တဲ့ Patient ID ကို ပြန်ထုတ်ယူခြင်း
        patient_id = patient_dict[selected]

        # လူနာ၏ ဆေးကုသမှု အခြေအနေများကို ရွေးချယ်ရန် Input အကွက်များ ဖန်တီးခြင်း
        # ART (Antiretroviral Therapy) ဆေးသောက်နေသလား၊ ကိုယ်ဝန်ရှိနေသလား စသည်တို့ကို ရွေးချယ်ခိုင်းခြင်း
        art = st.selectbox("ART Status", ["On ART", "Not on ART"])
        pregnancy = st.selectbox("Pregnancy Status", ["Yes", "No"])

        # Data သိမ်းဆည်းရန် ခလုတ်ဖန်တီးခြင်း (st.button ကို အသုံးပြုထားပါသည်)
        if st.button("Save Treatment", key="save_treatment_btn"):
            
            # မှတ်တမ်းအသစ်အတွက် ID အသစ်ဖန်တီးခြင်း
            # (လက်ရှိ Treatment ဇယားထဲမှာရှိတဲ့ အရေအတွက်ကို ယူပြီး ၁ ပေါင်းထည့်လိုက်ခြင်းဖြစ်သည်)
            next_treatment_id = len(treatment_df) + 1

            # Google Sheet ထဲကို ထည့်သွင်းမယ့် Data တွေကို ကော်လံအစဉ်လိုက်အတိုင်း စုစည်းခြင်း
            new_row = [
                next_treatment_id,
                patient_id,
                art,
                pregnancy
            ]

            # Google Sheet ဇယားရဲ့ အောက်ဆုံးစာကြောင်းမှာ Data သွားထည့်ပေးခြင်း
            treatment_sheet.append_row(new_row)

            # အောင်မြင်စွာ သိမ်းဆည်းပြီးကြောင်း အစိမ်းရောင်စာသားဖြင့် ပြသခြင်း
            st.success("✅ Treatment recorded successfully")
            
            # Data သစ်သွင်းပြီးတာနဲ့ စာမျက်နှာကို ချက်ချင်း Refresh (Update) ဖြစ်သွားအောင် ပြန်လည်စတင် (Rerun) ပေးခြင်း
            st.rerun()

except Exception as e:
    # Error တစ်ခုခု တက်ခဲ့ပါက User ကို အနီရောင်စာသားဖြင့် ပြသပေးခြင်း
    st.error(f"Error connecting to Google Sheets: {e}")
