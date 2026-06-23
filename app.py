import streamlit as st
import google.generativeai as genai

# إعداد واجهة الشات
st.set_page_config(page_title="SamiLab Agent", page_icon="🤖", layout="centered")
st.title("🤖 SamiLab AI Agent")
st.write("مرحباً بك يا سامي! الشات السحابي الخفيف راهو شغال بنجاح.")

# التحقق من وجود مفتاح الـ API في الإعدادات السرية للسحابة
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("خطأ: مفتاح الـ API غير مبرمج في الإعدادات السرية للسحابة (GEMINI_API_KEY).")
    st.stop()

# تهيئة ذاكرة الشات
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# استقبال رسالة جديدة من المستخدم
if prompt := st.chat_input("اكتب رسالتك هنا يا سامي..."):
    # عرض رسالة المستخدم فوراً
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        # استدعاء آخر موديل مستقر ومعتمد لعام 2026 مباشرة
        model = genai.GenerativeModel("gemini-2.5-flash")
        
        # طلب توليد المحتوى مع إرسال التوجيهات مباشرة لضمان اشتغاله
        response = model.generate_content(
            f"You are SamiLab AI Agent. Answer in Algerian Darja mixed with English naturally. User says: {prompt}"
        )
        
        # عرض رد الذكاء الاصطناعي
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        
    except Exception as e:
        st.error(f"حدث خطأ أثناء الاتصال بـ Gemini: {e}")
