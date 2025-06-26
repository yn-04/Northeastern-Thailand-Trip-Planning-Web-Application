from groq import Groq

# avaliable models
models = {
    "gemma2-9b-it": "gemma2-9b-it",
    "mixtral-8x7b-32768": "mixtral-8x7b-32768",
    "llama-3.2-1b-preview": "llama-3.2-1b-preview",
    "llama-3.2-3b-preview": "llama-3.2-3b-preview",
    "llama-3.1-8b-instant": "llama-3.1-8b-instant",
    "llama3-groq-8b-8192-tool-use-preview": "llama3-groq-8b-8192-tool-use-preview",
    "llama3-8b-8192": "llama3-8b-8192",
    "llama-3.2-11b-vision-preview": "llama-3.2-11b-vision-preview",
    "llama3-70b-8192": "llama3-70b-8192",
    "llama-3.3-70b-specdec": "llama-3.3-70b-specdec",
    "llama-3.3-70b-versatile": "llama-3.3-70b-versatile",
    "llama-3.1-70b-versatile": "llama-3.1-70b-versatile",
    "llama-3.2-90b-vision-preview": "llama-3.2-90b-vision-preview"
}

# api key
groq_client = Groq(
    api_key="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",
)

# agent requests
chat_completion = groq_client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "แนะนำสถานที่ท่องเที่ยวจังหวัดขอนแก่นในประเทศไทย ตอบเป็นภาษาไทยเท่านั้น โดยจัดแผนการท่องเที่ยวในจังหวัดขอนแก่นหลาย ๆ ตัวเลือก และข้อความมีความดึงดูดให้น่าอ่านน่าสนใจ ขอสำหรับการเที่ยว5วัน", # จะให้ agent ตอบแบบไหนอยู่ที่การตั้ง instruction ตรงนี้
        }
    ],
    model=models['llama3-70b-8192'],
)

# output
print(chat_completion.choices[0].message.content)