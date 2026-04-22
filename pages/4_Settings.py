# လိုအပ်တဲ့ Library များနှင့် Google Sheet ချိတ်ဆက်မယ့် Function ကို ခေါ်ယူခြင်း
import streamlit as st
import pandas as pd
from connection import get_google_sheet

# စာမျက်နှာရဲ့ ခေါင်းစဉ်ကို သတ်မှတ်ခြင်း
st.title("🏥 Facilities Management")

# Error တက်ခဲ့ပါက App မပျက်ကျစေရန် try-except ဖြင့် ကာကွယ်ခြင်း
try:
    # Google Sheets နှင့် ချိတ်ဆက်ခြင်း
    sheet = get_google_sheet()
    
    # "Facilities" (ဆေးရုံ/ဆေးခန်း) ဇယားကို လှမ်းဖတ်ပြီး Python DataFrame (ဇယား) အဖြစ် ပြောင်းခြင်း
    facilities_sheet = sheet.worksheet("Facilities")
    facilities_df = pd.DataFrame(facilities_sheet.get_all_records())

    # --- Data အသစ်ထည့်ရန် အပိုင်း ---
    # st.expander ဆိုတာက နှိပ်လိုက်မှ အောက်ကို ကျလာမယ့် (Dropdown ပုံစံ) အကွက်လေး ဖန်တီးတာပါ
    # စာမျက်နှာမှာ နေရာမယူဘဲ သပ်ရပ်နေစေဖို့ သုံးတာဖြစ်ပါတယ်
    with st.expander("Add New Facility"):
        # ဆေးရုံ/ဆေးခန်း နာမည်၊ မြို့နယ် နှင့် ပြည်နယ်/တိုင်း တို့ကို ရိုက်ထည့်ရန် စာရိုက်ကွက်များ ဖန်တီးခြင်း
        name = st.text_input("Facility Name")
        township = st.text_input("Township")
        state = st.text_input("State")

        # Data သိမ်းဆည်းရန် ခလုတ်ဖန်တီးခြင်း
        if st.button("Add Facility"):
            # .strip() ဆိုတာက User က စာမရိုက်ဘဲ Space bar (ကွက်လပ်) ကြီးပဲ ဖိနှိပ်ထားခဲ့ရင် 
            # အဲ့ဒီကွက်လပ်တွေကို ဖြတ်ထုတ်ပစ်လိုက်တာပါ။ 
            # ဖြတ်ထုတ်ပြီးတဲ့အချိန်မှာ (၃) ကွက်လုံးစာသားရှိနေသေးတယ် ဆိုမှသာ (True) အလုပ်လုပ်ပါမည်။
            if name.strip() and township.strip() and state.strip():
                
                # ID အသစ် သတ်မှတ်ခြင်း (လက်ရှိ ဆေးခန်းအရေအတွက်ကို ၁ ပေါင်းထည့်ခြင်း)
                next_id = len(facilities_df) + 1
                
                # Google Sheet ထဲသို့ Data အသစ်များ အစဉ်လိုက် သွားထည့်ခြင်း
                facilities_sheet.append_row([next_id, name, township, state])
                
                # အောင်မြင်ကြောင်း အစိမ်းရောင်စာသားဖြင့် ပြသခြင်း
                st.success("Facility added!")
                
                # ဇယားကို ချက်ချင်း Update ဖြစ်သွားအောင် စာမျက်နှာကို Refresh (Rerun) လုပ်ခြင်း
                st.rerun()
            else:
                # အကယ်၍ ကွက်လပ်တစ်ခုခုကို ချန်ထားခဲ့ပါက (သို့မဟုတ် Space တွေချည်းရိုက်ထားပါက) Error ပြခြင်း
                st.error("All fields are required")

    # --- လက်ရှိစာရင်းကို ပြသမည့် အပိုင်း ---
    st.subheader("Facilities List")
    # Data ဇယားကို မျက်နှာပြင်အပြည့်ဖြင့် ပြသခြင်း
    st.dataframe(facilities_df, use_container_width=True)

except Exception as e:
    # ချိတ်ဆက်မှု ပြဿနာရှိခဲ့ပါက Error ကို ပြသခြင်း
    st.error(f"Connection Error: {e}")
