from openai import OpenAI  # OpenAI Python library to make API calls
import requests  # used to download images
import os  # used to access filepaths
from PIL import Image  # used to print and edit images
from dotenv import load_dotenv
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
            "content": "แนะนำสถานที่ท่องเที่ยวจังหวัดพิษณุโลก Phitsanulok ในประเทศไทย เป็นภาษาไทย โดยจัดแผนการท่องเที่ยวในจังหวัดขอนแก่นหลาย ๆ ตัวเลือก และข้อความมีความดึงดูดให้น่าอ่านน่าสนใจ โดยออกมาเป็นโปสเตอร์รูปภาพ", # จะให้ agent ตอบแบบไหนอยู่ที่การตั้ง instruction ตรงนี้
        }
    ],
    model=models['llama-3.2-90b-vision-preview'],
)

# output
print(chat_completion.choices[0].message.content)

load_dotenv()
# initialize OpenAI client
print(os.environ.get("OPENAI_API_KEY"))
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# set the prompt
prompt = f"ขอเป็นรูปโปสเตอร์โปรโมทการท่องเที่ยวจังหวัด Phitsanulok โดยเป็นรูปโทนร้อน และตัวอักษรในรูปเป็นภาษาอังกฤษ {chat_completion.choices[0].message.content}"

# call the OpenAI API
generation_response = client.images.generate(
    model = "dall-e-3",
    prompt=prompt,
    n=1,
    size="1024x1792",
    response_format="url",
)

# print response
print(generation_response)

# create a directory to store the images into this working directory path
image_dir_name = "images"
image_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), image_dir_name)
if not os.path.isdir(image_dir):
    os.mkdir(image_dir)
    
# create the image file
generated_image_name = "generated_image.png"  # any name you like; the filetype should be .png
generated_image_filepath = os.path.join(image_dir, generated_image_name)

# generate the image
generated_image_url = generation_response.data[0].url  # extract image URL from response
generated_image = requests.get(generated_image_url).content  # download the image

# write image to file
with open(generated_image_filepath, "wb") as image_file:
    image_file.write(generated_image)  # write the image to the file
