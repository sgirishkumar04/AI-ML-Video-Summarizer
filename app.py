# app.py (Final Version: Multilingual Translation to English & Free Summarization)

import os
import requests # Used for making API calls to Hugging Face
from flask import Flask, request, jsonify, render_template
from moviepy import VideoFileClip
from faster_whisper import WhisperModel # The local, free speech-to-text model

# --- Configuration ---

# 1. WHISPER MODEL CONFIGURATION
# We use a multilingual model to detect and translate other languages.
# "small" offers a good balance of speed and accuracy.
# Other options: "base", "medium", "large-v3". Larger models are more accurate but much slower.
# The first time you run the script, this model will be downloaded automatically.
MODEL_SIZE = "tiny" 
print(f"Loading Whisper model: {MODEL_SIZE}...")
# device="cpu" and compute_type="int8" are optimizations for running on a standard computer.
whisper_model = WhisperModel(MODEL_SIZE, device="cpu", compute_type="int8")
print("Whisper model loaded successfully.")

# 2. HUGGING FACE API CONFIGURATION
# Your app needs this API token to use the free summarization service.
HF_API_TOKEN = os.getenv("HUGGING_FACE_HUB_TOKEN")
SUMMARIZATION_API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"

# 3. FLASK APP INITIALIZATION
app = Flask(__name__)
# Create a folder for temporary file uploads if it doesn't exist
if not os.path.exists('uploads'):
    os.makedirs('uploads')

# --- Helper Functions (The Core Logic) ---

def extract_audio_from_video(video_path):
    """Extracts the audio track from a video file and saves it as an MP3."""
    try:
        video_clip = VideoFileClip(video_path)
        audio_path = video_path + ".mp3"
        # logger=None prevents moviepy from printing progress bars to the console
        video_clip.audio.write_audiofile(audio_path, logger=None)
        video_clip.close()
        return audio_path
    except Exception as e:
        print(f"Error extracting audio: {e}")
        return None

def transcribe_and_translate_audio(audio_path):
    """
    Transcribes audio from any supported language and translates the output to English.
    """
    try:
        # The key change is task="translate", which tells Whisper to output in English.
        segments, info = whisper_model.transcribe(audio_path, beam_size=5, task="translate")
        
        # Log the detected language for debugging/verification
        print(f"Detected source language '{info.language}' with probability {info.language_probability}")
        
        # Join all the transcribed segments into a single string
        full_transcript = "".join(segment.text for segment in segments)
        return full_transcript.strip()
    except Exception as e:
        print(f"Error in transcription: {e}")
        return f"Transcription Error: {e}"

def summarize_text(text_to_summarize):
    """Summarizes the given text using the Hugging Face Inference API."""
    if not HF_API_TOKEN:
        return "Error: Hugging Face API token is not set. Please set the HUGGING_FACE_HUB_TOKEN environment variable."
        
    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
    
    # We create a JSON payload with the text and some parameters for the model
    payload = {
        "inputs": text_to_summarize,
        "parameters": {
            "max_length": 150,  # The maximum length of the summary
            "min_length": 30,   # The minimum length of the summary
            "do_sample": False
        }
    }
    
    try:
        response = requests.post(SUMMARIZATION_API_URL, headers=headers, json=payload)
        # Raise an exception if the API returns an error status code (e.g., 4xx, 5xx)
        response.raise_for_status() 
        
        summary = response.json()
        return summary[0]['summary_text'].strip()
    except requests.exceptions.RequestException as e:
        # Handle connection errors or bad responses from the API
        error_details = e.response.json().get('error', str(e)) if e.response else str(e)
        print(f"Error calling Hugging Face API: {error_details}")
        return f"Summarization Error: Could not connect to the API. Details: {error_details}"
    except Exception as e:
        print(f"An unexpected error occurred during summarization: {e}")
        return f"Summarization Error: An unexpected error occurred."

# --- Flask Routes (The Web Interface) ---

@app.route('/')
def index():
    """Serves the main HTML page of the application."""
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe_video_route():
    """Handles the video upload and returns the English transcript."""
    if 'video' not in request.files:
        return jsonify({"error": "No video file provided"}), 400

    video_file = request.files['video']
    
    # Securely save the uploaded file temporarily
    video_path = os.path.join('uploads', video_file.filename)
    video_file.save(video_path)

    # Process the video
    audio_path = extract_audio_from_video(video_path)
    if not audio_path:
        os.remove(video_path) # Clean up if audio extraction fails
        return jsonify({"error": "Failed to extract audio from video"}), 500

    transcript_text = transcribe_and_translate_audio(audio_path)

    # Clean up the temporary video and audio files
    os.remove(video_path)
    os.remove(audio_path)

    return jsonify({"transcript": transcript_text})

@app.route('/summarize', methods=['POST'])
def summarize_transcript_route():
    """Receives text from the frontend and returns its summary."""
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "No text was provided for summarization"}), 400

    text = data['text']
    summary_text = summarize_text(text)
    
    return jsonify({"summary": summary_text})

# --- Run the Application ---
if __name__ == '__main__':
    # threaded=True allows the app to handle multiple requests simultaneously
    app.run(debug=True, threaded=True)