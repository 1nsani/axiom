import os
import json
from pydantic import BaseModel, Field
from typing import List
import google.generativeai as genai

# Definisikan skema kaku (Ini adalah 'kontrak' data)
class ConceptSchema(BaseModel):
    objek: str
    massa: float
    gaya: float
    hukum_fisika: str

def get_ai_concept(text: str):
    # Konfigurasi API key dari environment variable
    genai.configure(api_key=os.environ["AIzaSyBbd23-Kns8CLylF8h7G7Vbg3J9rODY4Fg"])
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Memaksa AI mengikuti struktur Pydantic
    prompt = f"Ekstrak data dari soal berikut: {text}. Output harus JSON murni."
    
    # Panggilan AI
    response = model.generate_content(prompt)
    
    # Parsing hasil
    return json.loads(response.text)
  
