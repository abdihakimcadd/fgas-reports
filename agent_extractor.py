from openai import OpenAI
import os
import json

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def extract_fields(transcript_text):
    extraction_prompt = f"""
    You are an AI assistant for Italian HVAC technicians. 
    Extract the following 12 fields from the transcript of an F-Gas intervention.
    Return ONLY a valid JSON object with these exact keys. If a field is not mentioned, use "N/D".
    
    Transcript: "{transcript_text}"
    
    Keys:
    - cliente, indirizzo, tipo_impianto, marchio, modello, matricola, 
    - tipo_gas, quantita_gas_kg, tipo_intervento, esito, data_intervento, tecnico
    """
    
    chat_completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are a helpful HVAC compliance assistant that only outputs JSON."},
            {"role": "user", "content": extraction_prompt}
        ]
    )
    return json.loads(chat_completion.choices[0].message.content)
