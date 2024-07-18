import cv2
import pytesseract
import numpy as np
import base64
import os
from dotenv import load_dotenv
from Preprocess import Prprocess
import fireworks.client
import argparse
load_dotenv()

api_key = os.getenv('FIREWORK_AP_KEY')
fireworks.client.api_key = api_key

def encode_image(image):
    _, buffer = cv2.imencode('.jpg', image)
    return base64.b64encode(buffer).decode('utf-8')

def get_text_from_ocr(image):
    return pytesseract.image_to_string(image)

def gettext(img) : 

    response = fireworks.client.ChatCompletion.create (
    model = "accounts/fireworks/models/firellava-13b",
    messages = [{
        "role": "user",
        "content": [{
        "type": "text",
        "text": """
    Please analyze the following image of a passport or driver's license and extract the following information in JSON format: Try to get eye and hair color from image 

    1. Document Type (Passport/Driver's License) from the heading  2. Full Name (They are mostly in two lines) 3. Date of Birth  4. Document Number
    5. Issue Date 6. Expiration Date 7. Nationality (for passports) 8. Address (for driver's licenses) 9. Gender 10. Issuing Authority
    11. Eye and Hair Color 12. Height and Weight 13 Class (for driver's licenses)
    """ , }, {
        "type": "image_url",
        "image_url": {
            "url": f"data:image/jpeg;base64,{img}"
        },
        }, ],
    }],
    )
    string_vlm = response.choices[0].message.content
    return string_vlm

def correct_text(string_ocr, string_vlm):
    response = fireworks.client.ChatCompletion.create(
        model="accounts/fireworks/models/llama-v3-8b-instruct",
        messages=[
            {
                "role": "user",
                "content": f"""
# Correct any typos caused by bad OCR in this text. Don't change any information like name, number, etc. Respond only with the corrected text: {string_ocr}
You may use some data from {string_vlm} to correct additional information, but don't rely on it too much as it may make up some stuff. 
Please just give me output in the following format of JSON. Dont add any additional information. : 
1. Document Type (Passport/Driver's License):
2. Full Name:
3. Date of Birth:
4. Document Number:
5. Issue Date:
6. Expiration Date:
7. Nationality (for passports):
8. Address (for driver's licenses):
9. Gender:
10. Issuing Authority:
11. Eye and Hair Color (for driver's licenses):
12. Height and Weight (for driver's licenses):
13. Class (for driver's licenses):
"""
            }
        ]
    )
    return response.choices[0].message.content

def main(filePath):
    preprocess = Prprocess()
    image = cv2.imread(filePath)
    
    rotated_image = preprocess.rotate(image, 0)  
    cropped_image = preprocess.crop_area(rotated_image)
    
    image_base64 = encode_image(cropped_image)
    text_data = gettext(image_base64)
    ocr_text = get_text_from_ocr(cropped_image)
    final_text = correct_text(ocr_text, text_data)
    
    # Print corrected text
    print("Text From KYC : ")
    print(final_text)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process an ID.')
    parser.add_argument('file_path', type=str, help='Path to the image file')
    args = parser.parse_args()
    main(args.file_path) 


