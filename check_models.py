import google.generativeai as genai
import os

# Make sure to set your API key here or in your environment variables
os.environ["GOOGLE_API_KEY"] = "YOUR_ACTUAL_API_KEY"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

print("Listing available models...")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)