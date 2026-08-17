from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def transcribe_audio(audio_buffer):
    audio_buffer.name = "intervention.webm"
    transcription = client.audio.transcriptions.create(
        model="whisper-large-v3",
        file=audio_buffer,
        language="it"
    )
    return transcription.text
