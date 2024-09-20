import requests
import os


def upload_image_to_imgbb(image_file):
    imgbb_api_key = os.getenv('IMGBB_API_KEY')

    # Convert image to bytes
    image_data = image_file.read()

    # Upload image to Imgbb API
    url = 'https://api.imgbb.com/1/upload'
    payload = {
        'key': imgbb_api_key,
        'image': image_data.encode('base64'),  # Base64 encode image data
    }

    response = requests.post(url, data=payload)

    if response.status_code == 200:
        # Extract the image URL from the response
        return response.json()['data']['url']
    else:
        raise Exception(f"Failed to upload image to Imgbb: {response.text}")
