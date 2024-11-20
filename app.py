import streamlit as st
import requests
from gtts import gTTS
import os
import base64

# Set Cohere API key (Replace with your actual API key)
cohere_api_key = "9cXeu16WbLhcKXpfCjJspMsN9WLQY5zEIIaw77BB"

# Function to process text using Cohere
def cohere_process_text(prompt):
    url = "https://api.cohere.ai/generate"
    headers = {
        "Authorization": f"Bearer {cohere_api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "command",  # Specify the Cohere model
        "prompt": prompt,
        "max_tokens": 100,  # Adjust based on your needs
        "temperature": 0.5  # Control creativity
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('text', '').strip()
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error: {str(e)}"

# Function to convert text to speech and save it as an MP3 file
def text_to_speech(text, lang="en"):
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        audio_file = "output.mp3"
        tts.save(audio_file)
        return audio_file
    except Exception as e:
        return f"Error: {str(e)}"

# Function to generate a download link for the audio file
def generate_download_link(file_path):
    with open(file_path, "rb") as f:
        audio_bytes = f.read()
        b64 = base64.b64encode(audio_bytes).decode()
        href = f'<a href="data:audio/mp3;base64,{b64}" download="output.mp3">Download Speech</a>'
        return href

# Streamlit App Interface
st.set_page_config(page_title="Cohere Text-to-Speech App")
st.header("Cohere Text-to-Speech App")

# Input for text
input_text = st.text_area("Enter the text convert to speech:", key="input")

# Dropdown to select language
language = st.selectbox("Select Language for Speech Output", options=["en", "es", "fr", "de", "hi"], index=0)

# Button to trigger processing and TTS
submit = st.button("Convert to Speech")

# If the button is clicked and input text is provided
if submit and input_text:
    # Process the text with Cohere
    processed_text = input_text
    
    if "Error" not in processed_text:
        st.subheader("Processed Text:")
        st.write(processed_text)
        
        # Convert processed text to speech
        audio_file_path = text_to_speech(processed_text, lang=language)
        
        if os.path.exists(audio_file_path):
            # Audio Player
            st.audio(audio_file_path, format="audio/mp3")
            
            # Download Link
            st.markdown(generate_download_link(audio_file_path), unsafe_allow_html=True)
            
            # Remove the temporary file
            os.remove(audio_file_path)
        else:
            st.error(audio_file_path)  # Display error message if TTS failed
    else:
        st.error(processed_text)  # Display error message if Cohere processing failed
