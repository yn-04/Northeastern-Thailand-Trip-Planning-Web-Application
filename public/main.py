import streamlit as st
from PIL import Image
from groq import Groq
import os
from dotenv import load_dotenv
import base64
from huggingface_hub import InferenceClient

# === ตั้งค่าหน้าเว็บ ===
st.set_page_config(page_title="LUXURY TRAVEL GUIDE", page_icon="✨", layout="wide")

# === โหลด API Keys ===
load_dotenv()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# === กำหนด CSS สำหรับ Luxury Light UI ===
st.markdown(
    """
    <style>
    /* พื้นหลังสีขาวหรูหรา */
    .stApp {
        background: #F8F8F8; /* ขาว-ครีม */
        color: #333;
        font-family: 'Helvetica Neue', sans-serif;
    }

    /* Header Title */
    .header {
        text-align: center;
        font-size: 48px;
        font-weight: bold;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 40px;
        color: #222;
    }

    /* Luxury Form Container */

    /* ปุ่ม */
    .stButton > button {
        background: #222;
        color: white;
        font-size: 18px;
        border-radius: 30px;
        padding: 14px 35px;
        border: none;
        transition: all 0.3s ease-in-out;
        text-transform: uppercase;
        letter-spacing: 1px;
        display: block;
        margin: auto;
    }

    /* เอฟเฟกต์ปุ่ม Hover */
    .stButton > button:hover {
        background: #000;
        color: white;
        transform: scale(1.05);
    }

    /* กล่องแสดงผล */
    .result-box {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 16px;
        padding: 30px;
        margin-top: 30px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
        font-size: 20px;
    }

    /* รูปภาพ */
    .result-image {
        width: 100%;
        border-radius: 16px;
        margin-bottom: 20px;
    }

    /* Subheader */
    h3 {
        font-size: 26px;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #222;
        font-weight: bold;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# === Header ===
st.markdown("<h1 class='header'>TRAVEL GUIDE</h1>", unsafe_allow_html=True)

# === Input Form (Luxury Style) ===
st.markdown("<div class='form-container'>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    province = st.selectbox(" DESTINATION", ["ขอนแก่น", "นครพนม", "นครศรีธรรมราช", "บุรีรัมย์", "เลย"])
    days = st.number_input(" DAYS", min_value=1, step=1, value=3, format="%d")

with col2:
    activity_type = st.multiselect(" EXPERIENCE", ["ธรรมชาติ", "เมือง", "วัฒนธรรม", "เอกซ์ตรีม", "ชิล ๆ คาเฟ่"])
    budget = st.selectbox(" BUDGET", ["Low", "High"])

st.markdown("</div>", unsafe_allow_html=True)

# === ปุ่มค้นหา ===
st.markdown("<br>", unsafe_allow_html=True)
search = st.button("GET YOUR PLAN")

# === Helper Function: แปลงรูปภาพเป็น Base64 ===
def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# === Generate Image ===
def generate_image(prompt):
    image_dir_name = "images"
    image_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), image_dir_name)
    if not os.path.isdir(image_dir):
        os.mkdir(image_dir)
    
    client = InferenceClient(
        provider="hf-inference",
        api_key=os.getenv("HUGGINGFACE_API_KEY")
    )
    
    image = client.text_to_image(
        prompt,
        model="stabilityai/stable-diffusion-3.5-large-turbo"
    )
    
    image_path = os.path.join(image_dir, "generated_image.png")
    image.save(image_path)
    return image_path

# === แสดงผลลัพธ์ ===
if search:
    if not province or not days or not activity_type or not budget:
        st.error("⚠️ PLEASE FILL IN ALL FIELDS!")
    else:
        with st.spinner("⏳ CREATING YOUR ITINERARY..."):
            try:
                # === สร้างคำถามให้ AI ===
                query = f"""
                    ขอคำตอบเป็นภาษาไทย,
                    ช่วยแนะนำแผนการท่องเที่ยวในจังหวัด {province} 
                    สำหรับจำนวน {days} วัน งบประมาณ {budget} บาท 
                    และประเภทการเที่ยว {', '.join(activity_type)} 
                """
                
                chat_completion = groq_client.chat.completions.create(
                    messages=[{"role": "user", "content": query}],
                    model="deepseek-r1-distill-llama-70b",
                )
                
                travel_plan = chat_completion.choices[0].message.content
                print("================ travel_plan Thai ================", travel_plan)
                
                
                chat_completion_translator = groq_client.chat.completions.create(
                    messages=[{"role": "user", "content": f"Please translate this from Thai to only English for create a banner image promoting this {province} and add some emoji in this context: {travel_plan}"}],
                    model="gemma2-9b-it",
                )
                travel_plan_translate = f"{chat_completion_translator.choices[0].message.content}"
                print("================ Translate Thai to English ================", travel_plan_translate)
                # === Generate Image ===
                image_path = generate_image(travel_plan_translate)
                base64_image = encode_image_to_base64(image_path)

                # === แสดงผลลัพธ์ ===
                st.markdown("<h3>YOUR ITINERARY</h3>", unsafe_allow_html=True)
                st.markdown(
                    f"""
                    <div class='result-box' style='text-align: center;'>
                        <img src='data:image/png;base64,{base64_image}' style='width: 800px; height: 600px; border: 2px solid;' alt='Luxury Travel Image' class='result-image'>
                    </div>
                    <div class='result-box'>
                        <div>{travel_plan}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            except Exception as e:
                st.error(f"❌ ERROR: {e}")
