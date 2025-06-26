import streamlit as st
from PIL import Image
from groq import Groq
import openai
import os
from dotenv import load_dotenv
from openai import OpenAI


# === Set Layout of Streamlit ===
st.set_page_config(page_title="แนะนำแผนการท่องเที่ยว", page_icon="🌍", layout="wide")

# === Load API Keys ===
load_dotenv()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
openai_api_key = os.getenv("OPENAI_API_KEY")

# === Background Image ===
background_image_url = "https://cbtthailand.dasta.or.th/upload-file-api/Resources/RelateAttraction/Images/RAT400021/1.jpeg"

st.markdown(
    f"""
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css" rel="stylesheet">
    <style>
    .stApp {{
        background-image: url('{background_image_url}');
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
        font-family: 'Arial', sans-serif;
        color: #333;
    }}
    .spacing {{
        margin-top: 70px;
    }}
    .distance {{
        margin-top: 15px;
        margin-bottom: 0px;
        padding-bottom: 0px;
    }}
    .header {{
        text-align: center;
        margin-bottom: 30px;
    }}
    .result-box {{
        border: 2px solid #ddd;
        padding: 20px;
        border-radius: 12px;
        background-color: rgba(255, 255, 255, 0.75);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease-in-out;
    }}
    .result-box:hover {{
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    }}

    footer {{
        text-align: center;
        color: #777;
        font-size: 0.9rem;
        padding: 10px 0;
        background-color: rgba(0, 0, 0, 0.05);
        border-radius: 6px;
        margin-top: 40px;
    }}
    footer a {{
        color: #007bff;
        text-decoration: none;
    }}
    footer a:hover {{
        text-decoration: underline;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# === Header ===
st.markdown("<h1 class='header'>🌟 ระบบแนะนำแผนการท่องเที่ยว</h1>", unsafe_allow_html=True)

# === Input Form ===
with st.container():  # ใช้ container เป็นกล่องรอบคอลัมน์
    st.markdown('<div class="form-container">',unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 1.5])

    with col1:
        st.markdown("<div class='distance'><i class='bi bi-geo-alt'></i> Where to?</div>", unsafe_allow_html=True)
        province = st.selectbox("", ["ขอนแก่น", "นครพนม", "นครศรีธรรมราช", "บุรีรัมย์", "เลย"])

    with col2:
        st.markdown("<div class='distance'><i class='bi bi-calendar'></i> Days </div>", unsafe_allow_html=True)
        days = st.number_input("", min_value=1, step=1, value=3, format="%d")

    with col3:
        st.markdown("<div class='distance'><i class='bi bi-compass'></i> Types</div></div>",unsafe_allow_html=True,)
        activity_type = st.multiselect("", ["ธรรมชาติ", "เมือง", "วัฒนธรรม", "เอกซ์ตรีม", "ชิล ๆ คาเฟ่"])

    with col4:
        st.markdown("<div class='distance'><i class='bi bi-cash'></i> Price</div>", unsafe_allow_html=True)
        budget = st.selectbox("", ["Low to High", "Hight to Low"])
        

    with col5:
        st.markdown("<div class='spacing'></div>", unsafe_allow_html=True)
        search = st.button("Search", key="search")
    st.markdown("</div>", unsafe_allow_html=True) 

# === Process User Input ===
if search:
    if not province or not days or not activity_type or not budget:
        st.error("กรุณาเลือกข้อมูลให้ครบทุกช่องก่อนเริ่มค้นหา!")
    else:
        with st.spinner("กำลังประมวลผล..."):
            try:
                # === สร้างข้อความคำถามสำหรับ Groq ===
                query = f"""
                ช่วยแนะนำแผนการท่องเที่ยวในจังหวัด {province} 
                สำหรับจำนวน {days} วัน งบประมาณ {budget} บาท 
                และประเภทการเที่ยว {', '.join(activity_type)}
                """
                chat_completion = groq_client.chat.completions.create(
                    messages=[{"role": "user", "content": query}],
                    model="llama-3.1-70b-versatile",
                )

                # Show Result
                st.subheader("✨ แผนการท่องเที่ยวที่แนะนำ:")
                st.markdown(
                    f"<div class='result-box'><div style='color: black;'>{chat_completion.choices[0].message.content}</div></div>",
                    unsafe_allow_html=True,
                )

            except Exception as e:
                st.error(f"เกิดข้อผิด: {e}")

# === Footer ===
st.markdown(
    """
    <footer>
        © 2025 ระบบแนะนำแผนการท่องเที่ยว | พัฒนาโดย 
    </footer>
    """,
    unsafe_allow_html=True,
)
