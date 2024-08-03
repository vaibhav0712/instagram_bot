from instagrapi import Client # type: ignore
import requests

def publish_media(username, password, media_path, caption='wisemind motivation'):
    cl = Client()
    res = cl.login(username, password)
    print('Login : ', res)
    media = cl.photo_upload(media_path, caption)
    print('Media published')
    


def publish_media_graphapi(token, app_id, image_url):

    # 1. create media container 
    media_container_url = f"https://graph.facebook.com/v20.0/{app_id}/media"
    container_para = { "access_token":token, "image_url":image_url }
    container_res = requests.post(media_container_url, params=container_para)
    container_id = container_res.json()['id']
    print('container_id',container_id)

    # 2. publish media to instagram
    media_publish_url = f"https://graph.facebook.com/v20.0/{app_id}/media_publish"
    publish_para = {"creation_id": container_id, "access_token": token}
    publish_res = requests.post(media_publish_url, params=publish_para)
    print(publish_res.json())

