from create_post import create_instagram_post
from publish import publish_media, publish_media_graphapi
from datetime import date, datetime
import os
import base64
import requests

# Define the base directory (the directory where main.py is located)
base_dir = os.path.dirname(__file__)

# Use relative paths to reference the files
config_path = os.path.join(base_dir, "config.txt")
font_path = os.path.join(base_dir, "fonts/cooper/COOPBL.TTF")
daywise_text_path = os.path.join(base_dir, "quots/daywise.txt")


day = datetime.now().day
today = date.today()
username, password, token, app_id= open(config_path).read().splitlines()

image_number = day % 10
background_path = os.path.join(base_dir, f"images/{image_number}.jpg")
output_path = os.path.join(base_dir, f"generated_post/{today}.jpg")
daywise_text = open(daywise_text_path).read().splitlines()[day]


# generate instagram post(single image)
create_instagram_post(
    background_path,
    text=daywise_text,
    font_path=font_path,
    font_size=80,
    output_path=output_path,
)

# TODO: Need to find a way to upload generated post into some platform and get url of it
def upload_image(image_path):
    client_id = "b80b3c1cbef6b94"
    api_endpoint = "https://api.imgur.com/3/image"

    with open(image_path, 'rb') as image_file:
        image_data = base64.b64encode(image_file.read())

    headers = {'Authorization':f'Client-ID {client_id}'}
    data = {'image': image_data}

    response = requests.post(api_endpoint, headers=headers, data=data)

    if response.status_code == 200:
        return response.json()['data']['link']
    else:
        return None

image_url = upload_image(image_path = output_path)
print(image_url)

# upload via graphApi of Meta 
publish_media_graphapi(token, app_id, image_url)


# upload to instagram # will not work in cloud but work's fine in local
# publish_media(username, password, media_path=output_path, caption=daywise_text)
