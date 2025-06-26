# imports
from openai import OpenAI  # OpenAI Python library to make API calls
import requests  # used to download images
import os  # used to access filepaths
from PIL import Image  # used to print and edit images
from dotenv import load_dotenv

load_dotenv()
# initialize OpenAI client
print(os.environ.get("OPENAI_API_KEY"))
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# set the prompt
prompt = "รวมสถานที่ท่องเที่ยวในจังหวัดนครราชสีมาประเทศไทย"

# call the OpenAI API
generation_response = client.images.generate(
    model = "dall-e-3",
    prompt=prompt,
    n=1,
    size="1792x1024",
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
