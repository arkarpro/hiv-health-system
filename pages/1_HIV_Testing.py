# Streamlit (UI ဖန်တီးရန်) နှင့် Pandas (ဒေတာဇယားများ ကိုင်တွယ်ရန်) ကို ခေါ်ယူခြင်း
import streamlit as st
import pandas as pd
# ကျွန်တော်တို့ အရင်က ရေးထားတဲ့ connection ဖိုင်ထဲက Google Sheet ချိတ်ဆက်မယ့် Function ကို လှမ်းခေါ်ခြင်း
from connection import get_google_sheet

# စာမျက်နှာရဲ့ ခေါင်းစဉ်ကို သတ်မှတ်ခြင်း
st.title("🔬 HIV Testing")

# Error တက်ရင် App ကြီး ပျက်မကျသွားအောင် try-except block ဖြင့် အုပ်ထားခြင်း
try:
    # Google Sheets နှင့် ချိတ်ဆက်ခြင်း (connection.py မှ)
    sheet = get_google_sheet()

    # လူနာစာရင်း (Patients) ကို Google Sheet ထဲမှ လှမ်းဖတ်ပြီး ဇယား (DataFrame) အဖြစ် ပြောင်းခြင်း
    patients_sheet = sheet.worksheet("Patients")
    patients_df = pd.DataFrame(patients_sheet.get_all_records())
    # ကော်လံနာမည်တွေမှာ မလိုအပ်တဲ့ Space (ကွက်လပ်) တွေ ပါနေရင် ရှင်းလင်းပေးခြင်း
    patients_df.columns = patients_df.columns.str.strip()

    # ဆေးစစ်ချက်မှတ်တမ်း (HIV_Testing) ကို Google Sheet ထဲမှ လှမ်းဖတ်ခြင်း
    testing_sheet = sheet.worksheet("HIV_Testing")
    testing_df = pd.DataFrame(testing_sheet.get_all_records())

    # လူနာစာရင်းထဲမှာ Data မရှိရင် (ဗလာဖြစ်နေရင်) သတိပေးချက်ပြခြင်း
    if patients_df.empty:
        st.warning("⚠️ No patients found. Please add a patient in the Patient Management page first.")
    else:
        # User Interface - Form အသုံးပြုခြင်း (ခလုတ်နှိပ်မှသာ Data ကို တစ်ခါတည်း ပို့ရန် Form သုံးခြင်းဖြစ်သည်)
        with st.form("testing_form"):
            st.subheader("Record New Test Result")
            
            # လူနာရွေးချယ်ရန် Dropdown (ID နှင့် နာမည်ကို တွဲပြီး ပြသပေးရန် ဖန်တီးခြင်း)
            # ဥပမာ "1 - U Ba", "2 - Daw Hla" စသဖြင့် ပေါ်နေစေရန်
            patient_dict = {f"{row['patient_id']} - {row['name']}": row['patient_id'] for _, row in patients_df.iterrows()}
            selected = st.selectbox("Select Patient", list(patient_dict.keys()))
            
            # စစ်ဆေးသည့် ရက်စွဲနှင့် အဖြေ (Negative/Positive) ရွေးချယ်ရန် နေရာဖန်တီးခြင်း
            test_date = st.date_input("Test Date")
            result = st.selectbox("Result", ["Negative", "Positive"])
            
            # Data သိမ်းရန် ခလုတ် (Submit Button)
            submit = st.form_submit_button("Save Test Result")

            # ခလုတ်နှိပ်လိုက်ရင် အလုပ်လုပ်မယ့် အပိုင်း
            if submit:
                # ရွေးချယ်လိုက်တဲ့ လူနာရဲ့ ID အတိအကျကို ပြန်ယူခြင်း
                patient_id = patient_dict[selected]
                
                # ID အသစ်ပေးရန် (လက်ရှိရှိနေတဲ့ Data အရေအတွက်ကို ၁ ပေါင်းထည့်ခြင်း)
                next_test_id = len(testing_df) + 1

                # Google Sheet ထဲကို ထည့်သွင်းမယ့် Data တွေကို အစဉ်လိုက် စုစည်းခြင်း
                new_row = [
                    next_test_id,
                    patient_id,
                    str(test_date), # ရက်စွဲကို စာသား (String) အဖြစ် ပြောင်းသိမ်းမှ Sheet က လက်ခံပါမည်
                    result
                ]

                # Google Sheet ရဲ့ အောက်ဆုံးစာကြောင်းမှာ သွားထည့်ပေးခြင်း
                testing_sheet.append_row(new_row)
                st.success(f"✅ Test result for {selected} saved successfully!")
                
                # အကယ်၍ အဖြေသည် Positive ဖြစ်နေပါက နောက်တစ်ဆင့်အနေနဲ့ Treatment Page ကိုသွားရန် သတိပေးခြင်း
                if result == "Positive":
                    st.warning("🚨 Important: Patient is HIV Positive. Please proceed to the Treatment Page.")
                
                # Data သစ်သွင်းပြီးတာနဲ့ စာမျက်နှာကို Refresh လုပ်ပေးခြင်း (ဒါမှ အောက်က ဇယားမှာ ချက်ချင်း ပေါ်လာမည်)
                st.rerun()

    # လက်ရှိစစ်ဆေးပြီးသမျှ စာရင်းကို ပြသရန် အပိုင်း
    st.divider() # မျဉ်းတားပေးခြင်း
    st.subheader("Testing History")
    
    # မှတ်တမ်းရှိနေရင် ဇယားကို မျက်နှာပြင်အပြည့် (use_container_width=True) ဖြင့် ပြသခြင်း
    if not testing_df.empty:
        st.dataframe(testing_df, use_container_width=True)
    else:
        st.info("No testing records found.")

# အကယ်၍ အင်တာနက်မရှိတာ၊ Sheet ရှာမတွေ့တာမျိုး ဖြစ်ခဲ့ရင် Error ကို ပြသပေးခြင်း
except Exception as e:
    st.error(f"Error connecting to database: {e}")
