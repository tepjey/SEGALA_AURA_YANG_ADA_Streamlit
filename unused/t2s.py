import requests
import pygame

# Set your Eleven Labs API key
API_KEY = "sk_7a8dcaf7eb8639e2b7dede00a8472837e175cc73a9659453"

def text_to_speech(text):
    """Convert text to speech using Eleven Labs API with Jessica voice and Eleven Multilingual V2 model"""
    url = "https://api.elevenlabs.io/v1/text-to-speech/generate"
    
    # Prepare headers
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # Prepare request body with the new voice and model
    data = {
        "text": text,
        "voice": "jessica",  # Use Jessica's voice
        "model": "multilingual-v2",  # Use the Eleven Multilingual V2 model
        "speed": 1.0,  # Adjust speech speed
        "pitch": 1.0,  # Adjust pitch
    }

    # Send request to Eleven Labs API
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        # Get the audio content from the response
        audio_content = response.content

        # Save the audio to a file
        with open("output_audio.mp3", "wb") as audio_file:
            audio_file.write(audio_content)

        # Play the audio (optional, using Pygame for playback)
        pygame.mixer.init()
        pygame.mixer.music.load("output_audio.mp3")
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)  # Check if music is still playing
    else:
        print(f"Error: {response.status_code} - {response.text}")