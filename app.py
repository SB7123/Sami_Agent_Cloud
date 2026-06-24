import streamlit as str
import os
from groq import Groq

# إعداد واجهة المستخدم
str.set_page_config(page_title="SamiLab AI Agent", page_icon="🤖")
str.title("🤖 SamiLab AI Agent")

# جلب مفتاح API من Secrets
api_key = str.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")

if not api_key:
    str.error("خطأ: لم يتم العثور على مفتاح GROQ_API_KEY في الإعدادات!")
else:
    # تهيئة عميل Groq
    client = Groq(api_key=api_key)

    # تهيئة ذاكرة الشات
    if "messages" not in str.session_state:
        str.session_state.messages = []

    # عرض الرسائل السابقة
    for msg in str.session_state.messages:
        with str.chat_message(msg["role"]):
            str.markdown(msg["content"])

    # استقبال مدخلات المستخدم
    if prompt := str.chat_input("اكتب رسالتك هنا يا سامي..."):
        with str.chat_message("user"):
            str.markdown(prompt)
        str.session_state.messages.append({"role": "user", "content": prompt})

        # إرسال الطلب إلى Groq
        try:
            with str.chat_message("assistant"):
                response_placeholder = str.empty()
                full_response = ""
                
                completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": m["role"], "content": m["content"]} for m in str.session_state.messages],
                    stream=True,
                )
                
                for chunk in completion:
                    if chunk.choices[0].delta.content:
                        full_response += chunk.choices[0].delta.content
                        response_placeholder.markdown(full_response + "▌")
                
                response_placeholder.markdown(full_response)
                
            str.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            str.error(f"خطأ في الرد من الموديل: {e}")
