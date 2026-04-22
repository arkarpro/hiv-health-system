# Streamlit library ကို 'st' ဆိုတဲ့ နာမည်တိုလေးနဲ့ သုံးဖို့ ခေါ်လိုက်တာပါ။ (Web App ရဲ့ မျက်နှာစာ ဖန်တီးဖို့ သုံးပါတယ်)
import streamlit as st

# Google Sheets တွေကို Python ကနေ လွယ်လွယ်ကူကူ လှမ်းဖတ်/လှမ်းရေးလို့ရအောင် ကူညီပေးမယ့် Library ကို ခေါ်လိုက်တာပါ။
import gspread

# Google ရဲ့ လုံခြုံရေးစနစ် (Service Account) ကို ချိတ်ဆက်ဖို့အတွက် လိုအပ်တဲ့ အထောက်အထား (Credentials) အပိုင်းကို ခေါ်ယူတာပါ။
from google.oauth2.service_account import Credentials

# @st.cache_resource ဆိုတာက ဒီ Function ကို ခဏခဏ အလုပ်မလုပ်ခိုင်းဘဲ၊ တစ်ခါချိတ်ဆက်ပြီးတာနဲ့ 
# ရလာတဲ့ Connection ကို မှတ်ထားပေးဖို့ Streamlit ကို အမိန့်ပေးလိုက်တာပါ။ (App ကို သိသိသာသာ မြန်စေပါတယ်)
@st.cache_resource
def get_google_sheet():
    
    # ကိုယ့်ရဲ့ App က Google ရဲ့ ဘယ်နေရာတွေကို သုံးခွင့်/ဝင်ခွင့် (Access) လိုချင်တာလဲဆိုတဲ့ နယ်ပယ် (Scope) ကို သတ်မှတ်ပေးတာပါ။ 
    # ဒီမှာတော့ Google Sheets ဖတ်ဖို့နဲ့ Google Drive ထဲက ဖိုင်တွေကို ရှာဖို့ လင့်ခ် (၂) ခုကို ဝင်ခွင့်တောင်းထားတာပါ။
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    
    # Streamlit ရဲ့ လျှို့ဝှက်သေတ္တာ (st.secrets) ထဲမှာ သေချာဝှက်ပြီး သိမ်းထားတဲ့ 
    # Google လုံခြုံရေးသော့ (gcp_service_account) အချက်အလက်တွေကို လှမ်းယူပြီး ချိတ်ဆက်ဖို့ ပြင်ဆင်တာပါ။
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"], 
        scopes=scope
    )
    
    # အပေါ်က ယူလာတဲ့ သော့ (creds) ကိုသုံးပြီး Google ဆီမှာ တရားဝင် ဝင်ခွင့်တောင်း (Authorize လုပ်) လိုက်တာပါ။
    # client ဆိုတာက Google နဲ့ ကိုယ့် App ကြားမှာ အလုပ်လုပ်ပေးမယ့် ကိုယ်စားလှယ်လေးလို့ မှတ်ယူနိုင်ပါတယ်။
    client = gspread.authorize(creds)
    
    # ကိုယ်ဖွင့်ချင်တဲ့ Google Sheet ရဲ့ သီးသန့် ID (Key) အရှည်ကြီးကို ထည့်ပေးပြီး၊
    # ကိုယ်စားလှယ် (client) ကနေတစ်ဆင့် အဲ့ဒီ Sheet ကြီး တစ်ခုလုံးကို ဖွင့်ယူလိုက်တာပါ။
    sheet = client.open_by_key("1TPZTOzn7sG32OQKy2XwS_oOwtRiRHfCMoY40oovbBYs")
    
    # ချိတ်ဆက်လို့ အောင်မြင်သွားတဲ့အခါ အဲ့ဒီ Sheet ကြီးကို တခြားစာမျက်နှာတွေမှာ 
    # အလွယ်တကူ ဆက်သုံးလို့ရအောင် ဒီ Function ကနေ ပြန်ထုတ် (Return) ပေးလိုက်တာပါ။
    return sheet
