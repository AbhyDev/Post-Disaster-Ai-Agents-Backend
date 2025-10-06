import google.generativeai as genai
from PIL import Image
import os

from dotenv import load_dotenv
import os
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel('gemini-1.5-flash')

def detect_city_with_red_cross(image_path):
    image = Image.open(image_path)
    
    prompt = """
    Analyze this satellite image and:
    Look for a red cross marker
    Tell me which city name appears near or below the red cross    
    Focus especially on finding the city name that's positioned near the red cross marker. 1 work of city ONLY.
    """
    
    response = model.generate_content([prompt, image])
    
    return response.text

try:
    result = detect_city_with_red_cross("DummySatelliteImage.png")
    print("Gemini's analysis:")
    print(result)
except Exception as e:
    print(f"Error: {e}")