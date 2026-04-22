# Streamlit library ကို 'st' ဆိုတဲ့ နာမည်တိုလေးနဲ့ သုံးဖို့ ခေါ်လိုက်တာပါ။
import streamlit as st

# st.set_page_config ဆိုတာ Web Browser ရဲ့ အပေါ်ဆုံး Tab လေးမှာပေါ်မယ့် နာမည် (page_title) နဲ့ 
# Webpage ကြီးတစ်ခုလုံးရဲ့ အကျယ်အဝန်း (layout) ကို သတ်မှတ်ပေးတာပါ။ 
# "wide" လို့ ပေးထားတဲ့အတွက် ဖန်သားပြင်အပြည့် ကျယ်ကျယ်ဝန်းဝန်းလေး မြင်ရမှာဖြစ်ပါတယ်။
# (မှတ်ချက် - ဒီ Code ကြောင်းက တခြား Streamlit code တွေအားလုံးရဲ့ အပေါ်ဆုံး (ပထမဆုံး) မှာ အမြဲရှိနေရပါမယ်)
st.set_page_config(page_title="HIV System", layout="wide")

# st.title ဆိုတာက Webpage ရဲ့ အဓိက ခေါင်းစဉ်ကြီး (Heading) ကို အကြီးဆုံး စာလုံးအရွယ်အစားနဲ့ ဖော်ပြပေးတာပါ။
st.title("HIV Health Information System")

# st.write ဆိုတာကတော့ သာမန် စာပိုဒ်၊ စာသားလေးတွေကို Webpage ပေါ်မှာ ရေးပြချင်တဲ့အခါ သုံးပါတယ်။
st.write("Welcome to the HIV Health Information System")

# st.info ဆိုတာက အသိပေးချက် (သို့မဟုတ်) လမ်းညွှန်ချက်လေးတွေကို 
# အပြာရောင် နောက်ခံကွက်လေးနဲ့ သပ်သပ်ရပ်ရပ် ပေါ်လာအောင် (User တွေ မျက်စိကျသွားအောင်) ပြသပေးတာပါ။
st.info("Select a page from the sidebar to get started")
