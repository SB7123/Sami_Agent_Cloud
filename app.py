import streamlit as st
import requests

st.title("🤖 SamiLab AI Agent")

api_key = st.secrets.get("GEMINI_API_KEY")
prompt = st.chat_input("اكتب رسالتك هنا يا سامي...")

if prompt:
    st.write(f"أنت: {prompt}")
    
    # رابط الـ API المباشر
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
    
    headers = {'Content-Type': 'application/json'}
    data = {"contents": [{"parts": [{"text": f"Answer in Algerian Darja: {prompt}"}]}]}
    
    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        
        if "candidates" in result:
            reply = result["candidates"][0]["content"]["parts"][0]["text"]
            st.write(f"الوكيل: {reply}")
        else:
            st.error(f"خطأ من قوقل: {result}")
    except Exception as e:
        st.error(f"حدث خطأ في الاتصال: {e}")
