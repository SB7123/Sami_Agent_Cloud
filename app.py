import streamlit as st
import requests

st.set_page_config(page_title="SamiLab Agent", page_icon="🤖")
st.title("🤖 SamiLab AI Agent")

api_key = st.secrets.get("GEMINI_API_KEY")

# تهيئة ذاكرة الشات
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# استقبال الرسالة الجديدة
if prompt := st.chat_input("اكتب رسالتك هنا يا سامي..."):
    # عرض رسالة المستخدم
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    try:
        # 1. جلب اسم الموديل الشغال أوتوماتيكيا من سيرفر قوقل بناءً على المفتاح تاعك
        list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
        list_res = requests.get(list_url).json()
        
        working_model = None
        if "models" in list_res:
            for m in list_res["models"]:
                # نحوسو على أول موديل يدعم توليد النصوص ونهربو بيه
                if "generateContent" in m.get("supportedGenerationMethods", []):
                    working_model = m["name"]
                    break 
        
        # إذا السيرفر قال بلي المفتاح ما عندو حتى موديل
        if not working_model:
            st.error("للأسف، السيرفر أكد بلي هاد المفتاح ما عندوش أي صلاحية. لازم تفتح حساب قوقل جديد وتجيب مفتاح AIzaSy.")
            st.stop()

        # 2. إرسال الرسالة للموديل اللي تم اكتشافه بنجاح
        url = f"https://generativelanguage.googleapis.com/v1beta/{working_model}:generateContent?key={api_key}"
        headers = {'Content-Type': 'application/json'}
        data = {"contents": [{"parts": [{"text": f"You are SamiLab AI. Answer in Algerian Darja naturally. User says: {prompt}"}]}]}
        
        response = requests.post(url, headers=headers, json=data).json()
        
        # 3. عرض الرد
        with st.chat_message("assistant"):
            if "candidates" in response:
                reply = response["candidates"][0]["content"]["parts"][0]["text"]
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            else:
                st.error(f"خطأ في الرد من الموديل ({working_model}): {response}")
                
    except Exception as e:
        st.error(f"حدث خطأ في الاتصال: {e}")
