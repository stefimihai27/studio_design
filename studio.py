import streamlit as st
import requests
from io import BytesIO
from PIL import Image
import time
import random

# --- 1. CONFIGURARE PAGINĂ ---
st.set_page_config(page_title="Studio Design", page_icon="🎨", layout="centered")

# --- 2. CONFIGURARE API (PLAN B - HUGGING FACE) ---
# Cheia ta este aici pentru siguranță
hf_token = "hf_" + "QBRsrwvJvMTHLCUkSZqjadBoKJqejxqtvk"

# --- 3. FUNCTIILE DE GENERARE ---

def generate_with_pollinations(prompt):
    """Încearcă prima dată pe serverul public (Flux)"""
    try:
        # Folosim modelul FLUX (poate 'turbo' e scos) și nologo=false
        seed = random.randint(0, 100000)
        url = f"https://image.pollinations.ai/prompt/{prompt}?model=flux&width=1024&height=1024&seed={seed}&nologo=false"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            # VERIFICARE ANTI-EROARE: 
            # Imaginile de eroare ("We Moved") sunt mici (<10KB). Imaginile reale au >20KB.
            if len(response.content) > 15000:
                return Image.open(BytesIO(response.content)), "Pollinations (Flux)"
    except:
        pass
    return None, None

def generate_with_huggingface(prompt):
    """Planul de rezervă solid: Hugging Face cu cheia ta"""
    # Folosim SD v1.5 care este cel mai stabil model de pe planetă
    api_url = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
    headers = {"Authorization": f"Bearer {hf_token}"}
    
    try:
        # Încercăm de 3 ori (pentru că serverele pot fi "Loading")
        for i in range(3):
            response = requests.post(api_url, headers=headers, json={"inputs": prompt}, timeout=20)
            
            if response.status_code == 200:
                return Image.open(BytesIO(response.content)), "Stable Diffusion v1.5"
            
            # Dacă serverul se încarcă, așteptăm
            error = response.json()
            if "estimated_time" in error:
                time.sleep(error["estimated_time"])
            else:
                time.sleep(2)
                
    except:
        pass
    return None, None

# --- 4. INTERFAȚA VIZUALĂ ---
st.markdown("""
    <style>
        .stApp { background-color: #2c0710; }
        [data-testid="stSidebar"] { background-color: #3d0a16; }
        h1 { color: #ff1a4d !important; font-family: 'Helvetica', sans-serif; font-weight: 300; }
        h2, h3, p, label, .stMarkdown { color: #ffccd5 !important; }
        .stTextInput > div > div > input, .stTextArea > div > div > textarea {
             background-color: #5e1223 !important; color: white !important; border: 1px solid #ff1a4d; }
        .stButton > button {
            background-color: #ff1
