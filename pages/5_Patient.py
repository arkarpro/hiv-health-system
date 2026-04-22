# လိုအပ်တဲ့ Library များနှင့် Google Sheet ချိတ်ဆက်မယ့် Function ကို ခေါ်ယူခြင်း
import streamlit as st
import pandas as pd
from connection import get_google_sheet

# စာမျက်နှာရဲ့ ခေါင်းစဉ်ကို သတ်မှတ်ခြင်း
st.title("👥 Patient Management")

# Error တက်ခဲ့ပါက App မပျက်ကျစေရန် try-except ဖြင့် အုပ်ထားခြင်း
try:
    # Google Sheets နှင့် ချိတ်ဆက်ခြင်း
    sheet_file = get_google_sheet()
    
    # "Patients" (လူနာစာရင်း) ဇယားကို လှမ်းဖတ်ခြင်း
    patients_sheet = sheet_file.worksheet("Patients")
    
    # --- အချက်အလက်များ (Data) ကို ရယူခြင်းနှင့် သန့်စင်ခြင်း ---
    data = patients_sheet.get_all_records()
    # ရလာတဲ့ Data တွေကို Python Pandas ဇယား (DataFrame) အဖြစ် ပြောင်းလဲခြင်း
    existing_data = pd.DataFrame(data)
    # ကော်လံနာမည်တွေမှာ မလိုအပ်တဲ့ Space (ကွက်လပ်) တွေ ပါနေရင် ဖယ်ရှားရှင်းလင်းပေးခြင်း
    existing_data.columns = existing_data.columns.str.strip()

    # --- လူနာသစ် မှတ်ပုံတင်ရန် Form ဖန်တီးခြင်း ---
    # Form သုံးထားတဲ့အတွက် "Save Patient" ခလုတ်နှိပ်မှသာ Data ကို တစ်ပြိုင်နက်တည်း ပို့ပေးမည်ဖြစ်သည်
    with st.form("patient_form"):
        # လူနာအမည်၊ လိင် နှင့် အသက် ကို ထည့်သွင်းရန် အကွက်များ ဖန်တီးခြင်း
        name = st.text_input("Name")
        sex = st.selectbox("Sex", ["Male", "Female", "Other"])
        # အသက်ကို ဂဏန်း (Number) သီးသန့်ပဲ ရိုက်ထည့်ခွင့်ပေးပြီး၊ ၀ ကနေ ၁၂၀ ကြားပဲ လက်ခံမည်ဟု သတ်မှတ်ခြင်း
        age = st.number_input("Age", 0, 120)
        
        # Data သိမ်းဆည်းရန် ခလုတ် (Submit Button)
        submit = st.form_submit_button("Save Patient")

        # "Save Patient" ခလုတ်ကို နှိပ်လိုက်ပါက-
        if submit:
            # ၁။ အမည် ထည့်သွင်းထားခြင်း ရှိ/မရှိ စစ်ဆေးခြင်း
            if name.strip() == "":
                # အမည်မပါပါက Error စာသားပြခြင်း
                st.error("Name is required")
            
            # ၂။ အသက် မှန်ကန်မှု ရှိ/မရှိ စစ်ဆေးခြင်း
            elif age <= 0:
                # အသက်က သုည သို့မဟုတ် အနှုတ်ပြနေပါက Error ပြခြင်း
                st.error("Please enter a valid age")
            
            # ၃။ အချက်အလက်အားလုံး ပြည့်စုံမှန်ကန်မှသာ အောက်ပါအတိုင်း Data သိမ်းပေးခြင်း
            else:
                # လူနာ ID အသစ် သတ်မှတ်ခြင်း (လက်ရှိလူနာ အရေအတွက်ကို ၁ ပေါင်းထည့်ခြင်း)
                new_row = [len(existing_data) + 1, name, sex, age]
                
                # Google Sheet ရဲ့ "Patients" ဇယားအောက်ဆုံးတွင် သွားထည့်ခြင်း
                patients_sheet.append_row(new_row)
                
                # အောင်မြင်ကြောင်း အစိမ်းရောင်စာသားဖြင့် ပြသခြင်း
                st.success(f"✅ {name} added successfully")
                
                # ဇယားကို ချက်ချင်း Update ဖြစ်သွားအောင် စာမျက်နှာကို Refresh (Rerun) လုပ်ခြင်း
                st.rerun()

    # --- လက်ရှိ လူနာစာရင်းကို ပြသမည့် အပိုင်း ---
    st.subheader("Current Patient List")
    # လူနာစာရင်း ဇယားကို မျက်နှာပြင်အပြည့် (use_container_width=True) ဖြင့် ပြသခြင်း
    st.dataframe(existing_data, use_container_width=True)

except Exception as e:
    # ပြဿနာတစ်စုံတစ်ရာ ရှိခဲ့ပါက Error စာသားကို အနီရောင်ဖြင့် ပြသပေးခြင်း
    st.error(f"Error: {e}")
