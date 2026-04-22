# UI နှင့် ဂရပ်များဖန်တီးရန် Streamlit, Data များ တွက်ချက်ရန် Pandas ကို ခေါ်ယူခြင်း
import streamlit as st
import pandas as pd
# ချိတ်ဆက်ထားသော Google Sheet ကို လှမ်းခေါ်ခြင်း
from connection import get_google_sheet

# စာမျက်နှာရဲ့ ခေါင်းစဉ်ကို Dashboard ဟု သတ်မှတ်ခြင်း
st.title("📊 Dashboard")

# Error တက်ခဲ့ပါက App မပျက်ကျစေရန် try-except block ဖြင့် အုပ်ထားခြင်း
try:
    # Google Sheets နှင့် ချိတ်ဆက်ခြင်း
    sheet = get_google_sheet()

    # Google Sheets ထဲမှ "HIV_Testing" နှင့် "Treatment" ဇယားများကို လှမ်းဖတ်ပြီး 
    # Pandas DataFrame (Python ဇယား) အဖြစ် ပြောင်းလဲယူခြင်း
    testing = pd.DataFrame(sheet.worksheet("HIV_Testing").get_all_records())
    treatment = pd.DataFrame(sheet.worksheet("Treatment").get_all_records())

    # ဇယားထဲမှာ Data ရှိနေခဲ့ရင် ကော်လံ (Column) နာမည်တွေမှာ မတော်တဆ ပါလာတတ်တဲ့ 
    # Space (ကွက်လပ်) တွေကို ဖယ်ရှားရှင်းလင်းပေးခြင်း (Error မတက်အောင် ကာကွယ်ခြင်းဖြစ်သည်)
    if not testing.empty: testing.columns = testing.columns.str.strip()
    if not treatment.empty: treatment.columns = treatment.columns.str.strip()

    # --- ကိန်းဂဏန်းများ ပြသမည့် အပိုင်း ---
    # စာမျက်နှာကို ဘယ်၊ လယ်၊ ညာ ဆိုပြီး ကော်လံ (၃) ခု အညီအမျှ ခွဲလိုက်ခြင်း
    col1, col2, col3 = st.columns(3)

    # ပထမ ကော်လံ (ဘယ်ဘက်) တွင်-
    with col1:
        # ဆေးစစ်ထားသူ စုစုပေါင်း အရေအတွက်ကို ပြသခြင်း 
        # (testing ဇယားထဲမှာရှိတဲ့ အတန်းအရေအတွက် (len) ကို ရေတွက်ပြသခြင်းဖြစ်သည်)
        st.metric("Total Tested", len(testing))
    
    # ဒုတိယ ကော်လံ (အလယ်) တွင်-
    with col2:
        # Data လည်းရှိမယ်၊ "result" ဆိုတဲ့ ကော်လံလည်း ရှိမယ်ဆိုမှ အောက်ကစာကြောင်းကို အလုပ်လုပ်မည်
        if not testing.empty and "result" in testing.columns:
            # "result" ကော်လံထဲမှာ "Positive" လို့ ရေးထားတဲ့ လူအရေအတွက်ကို စစ်ထုတ်ပြီး ပြသခြင်း
            st.metric("Positive Cases", len(testing[testing["result"] == "Positive"]))
    
    # တတိယ ကော်လံ (ညာဘက်) တွင်-
    with col3:
        # Data လည်းရှိမယ်၊ "ART_status" ဆိုတဲ့ ကော်လံလည်း ရှိမယ်ဆိုမှ အလုပ်လုပ်မည်
        if not treatment.empty and "ART_status" in treatment.columns:
            # "ART_status" ထဲမှာ "On ART" (ဆေးသောက်နေသူ) အရေအတွက်ကို စစ်ထုတ်ပြီး ပြသခြင်း
            st.metric("On ART", len(treatment[treatment["ART_status"] == "On ART"]))

    # အပေါ်က ကိန်းဂဏန်းတွေနဲ့ အောက်က ဂရပ်တွေကြားမှာ မျဉ်းတစ်ကြောင်းတားပေးခြင်း
    st.divider()

    # --- ဂရပ် (Charts) များ ပြသမည့် အပိုင်း ---
    # စာမျက်နှာကို ဘယ်၊ ညာ ကော်လံ (၂) ခု ထပ်ခွဲလိုက်ခြင်း
    c1, c2 = st.columns(2)
    
    # ဘယ်ဘက် ကော်လံတွင်-
    with c1:
        if not testing.empty and "result" in testing.columns:
            st.subheader("Testing Results")
            # "result" ကော်လံထဲမှာ Positive ဘယ်နှစ်ယောက်၊ Negative ဘယ်နှစ်ယောက် ရှိလဲဆိုတာကို 
            # ရေတွက် (value_counts) ပြီး Bar Chart (ဘားဂရပ်) အဖြစ် အလိုအလျောက် ဆွဲပေးခြင်း
            st.bar_chart(testing["result"].value_counts())

    # ညာဘက် ကော်လံတွင်-
    with c2:
        if not treatment.empty and "ART_status" in treatment.columns:
            st.subheader("ART Status Distribution")
            # ဆေးသောက်နေသူ (On ART) နှင့် မသောက်သူ (Not on ART) အရေအတွက်ကို Bar Chart ဆွဲပြခြင်း
            st.bar_chart(treatment["ART_status"].value_counts())

# ပြဿနာတစ်စုံတစ်ရာ ရှိခဲ့ပါက Error စာသားကို အနီရောင်ဖြင့် ပြသပေးခြင်း
except Exception as e:
    st.error(f"Error loading dashboard: {e}")
