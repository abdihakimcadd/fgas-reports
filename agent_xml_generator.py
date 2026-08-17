import xml.etree.ElementTree as ET
import io
from supabase import create_client, Client
import os

supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

def generate_and_upload(extracted_data, user_id):
    root = ET.Element("ComunicazioneIntervento")
    for key, value in extracted_data.items():
        child = ET.SubElement(root, key)
        child.text = str(value)
        
    xml_str = ET.tostring(root, encoding='utf-8', xml_declaration=True)
    xml_buffer = io.BytesIO(xml_str)
    
    file_name = f"FGas_{user_id}_{extracted_data.get('data_intervento', 'unknown')}.xml"
    supabase.storage.from_("fgas-reports").upload(
        file_name,
        xml_buffer,
        file_options={"content-type": "application/xml", "upsert": "true"}
    )
    return supabase.storage.from_("fgas-reports").get_public_url(file_name)
