from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import io
from dotenv import load_dotenv

# Import your Agents
from agent_transcriber import transcribe_audio
from agent_extractor import extract_fields
from agent_xml_generator import generate_and_upload

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# ENDPOINT 1: Voice to Extracted Fields
# ==========================================
@app.post("/api/transcribe-and-extract")
async def transcribe_and_extract(file: UploadFile = File(...)):
    """
    Receives audio, returns transcript and 12 extracted fields.
    DOES NOT generate the XML yet. Waits for user confirmation.
    """
    try:
        # 1. Read audio bytes
        audio_bytes = await file.read()
        audio_buffer = io.BytesIO(audio_bytes)
        
        # 2. Agent 1: Transcribe
        transcript = transcribe_audio(audio_buffer)
        print(f"Transcript: {transcript}")

        # 3. Agent 2: Extract Fields
        fields = extract_fields(transcript)
        print(f"Extracted: {fields}")

        # 4. Return to Frontend for User Review
        return {
            "transcript": transcript,
            "fields": fields
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {"error": str(e)}


# ==========================================
# ENDPOINT 2: Generate XML (After User Confirms)
# ==========================================
class XMLRequest(BaseModel):
    confirmed_fields: dict
    user_id: str

@app.post("/api/generate-xml")
async def generate_xml_endpoint(request: XMLRequest):
    """
    Receives the confirmed/edited fields from the frontend, 
    generates the XML, and uploads to Supabase.
    """
    try:
        # 1. Agent 3: Generate & Upload XML
        xml_url = generate_and_upload(request.confirmed_fields, request.user_id)
        
        return {
            "success": True,
            "xml_url": xml_url
        }

    except Exception as e:
        print(f"Error generating XML: {str(e)}")
        return {"error": str(e)}
