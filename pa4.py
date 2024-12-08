import streamlit as st
import openai
import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import os

# ใช้ Environment Variable สำหรับ API Key
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    st.error("กรุณาตั้งค่า OpenAI API Key ใน Environment Variables")
else:
    openai.api_key = openai_api_key

# ส่วนการทำงานของแอป
st.title("Japanese Content Analyzer")
user_input = st.text_area("กรอกข้อความหรือใส่ลิงก์ภาษาญี่ปุ่นที่นี่:")

if st.button("เริ่มวิเคราะห์"):
    if user_input:
        parsed = urlparse(user_input)
        if parsed.scheme and parsed.netloc:
            try:
                response = requests.get(user_input)
                soup = BeautifulSoup(response.text, 'html.parser')
                content = soup.find('body')  # ดึงเนื้อหาหลัก
                japanese_text = content.get_text(strip=True) if content else None
                if not japanese_text:
                    st.error("ไม่สามารถดึงข้อมูลจากลิงก์นี้ได้")
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาด: {e}")
        else:
            japanese_text = user_input

        if japanese_text:
            st.write("### ข้อความที่วิเคราะห์:")
            st.write(japanese_text)

            # แปลข้อความ
            translation_prompt = f"แปลข้อความนี้จากภาษาญี่ปุ่นเป็นภาษาไทย:\n{japanese_text}"
            translation = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": translation_prompt}]
            )['choices'][0]['message']['content']
            st.write("### การแปล:")
            st.write(translation)
