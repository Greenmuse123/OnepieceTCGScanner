import os
import requests

# Download the image to the 'data/card_images' directory
def download_image(card_name, img_url):
    try:
        img_data = requests.get(img_url).content
        img_filename = f"data/card_images/{card_name.replace(' ', '_').replace('/', '_')}.jpg"  # Avoid spaces and special chars in filenames
        with open(img_filename, 'wb') as img_file:
            img_file.write(img_data)
        return img_filename
    except Exception as e:
        print(f"Error downloading image for {card_name}: {e}")
        return None
