import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# Google Sheets ချိတ်ဆက်မှုကို တစ်ကြိမ်ပဲလုပ်ပြီး မှတ်ထားပေးမယ့် Function
@st.cache_resource
def get_google_sheet():
    # scope သတ်မှတ်ခြင်း
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    
    # st.secrets ထဲကနေ Credential အချက်အလက်ယူခြင်း
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"], 
        scopes=scope
    )
    
    # Google Sheets ကို Authorize လုပ်ခြင်း
    client = gspread.authorize(creds)
    
    # Spreadsheet ကို Key ဖြင့် ဖွင့်ခြင်း
    sheet = client.open_by_key("1kgbCBC0jzEsmMdyrCpw1uHtF33qhMGmwQRlSNrUau10")
    
    return sheet
  
