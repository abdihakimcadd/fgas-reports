import xml.etree.ElementTree as ET
from supabase import create_client, Client
import os

supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

def generate_and_upload(extracted_data, user_id):
    """
    Agent 3: Receives JSON fields, generates XML, uploads to Supabase.
    """
    # 1. Build XML Tree
    root = ET.Element("ComunicazioneIntervento")
    for key, value in extracted_data.items():
        child = ET.SubElement(root, key)
        child.text = str(value)
        
    # Convert XML tree to raw bytes
    xml_bytes = ET.tostring(root, encoding='utf-8', xml_declaration=True)
    
    # 2. Upload to Supabase Storage
    file_name = f"FGas_{user_id}_{extracted_data.get('data_intervento', 'unknown')}.xml"
    supabase.storage.from_("fgas-reports").upload(
        file_name,
        xml_bytes,  # <--- CHANGED FROM xml_buffer TO xml_bytes
        file_options={"content-type": "application/xml", "upsert": "true"}
    )
    
    # 3. Return Public URL
    return supabase.storage.from_("fgas-reports").get_public_url(file_name)
