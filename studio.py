import streamlit as st
import requests
from io import BytesIO
from PIL import Image
import time
import random

# --- 1. CONFIGURARE PAGINĂ ---
st.set_page_config(page_title="Studio Design", page_icon="🎨", layout="centered")

# --- 2. CHEIA TA SECRETĂ (HUGGING FACE) ---
# O păstrăm ca metodă principală, e cea mai sigură.
hf_token = "hf_" + "QBRsrwvJvMTHLCUkSZqjadBoKJqejxqtvk"

# --- 3. FUNCȚIILE DE GENERARE ---

def generate_with_huggingface(prompt):
    """Metoda 1: Server Privat (Fără Logo, Fără Plată)"""
    # Folosim Stable Diffusion 1.5 care este stabil și gratuit pe API
    api_url = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
    headers = {"Authorization": f"Bearer {hf_token}"}
    
    try:
        # Încercăm de 2 ori, poate serverul e în "cold boot"
        for i in range(2):
            response = requests.post(api_url, headers=headers, json={"inputs": prompt}, timeout=20)
            if response.status_code == 200:
                return Image.open(BytesIO(response.content)), "Stable Diffusion v1.5 (Privat)"
            elif "loading" in response.text.lower():
                time.sleep(3) # Așteptăm să se trezească serverul
            else:
                break
    except Exception as e:
        pass
    return None, None

def generate_browser_link_flux(prompt):
    """Metoda 2: Browser Direct (Model FLUX - Gratuit)"""
    # ATENȚIE: Am schimbat 'turbo' cu 'flux' pentru că turbo cere bani acum.
    seed = random.randint(0, 1000000)
    # nologo=False înseamnă că acceptăm logo-ul mic ca să fie gratis
    return f"https://image.pollinations.ai/prompt/{prompt}?model=flux&width=1024&height=1024&seed={seed}&nologo=false"

# --- 4. DESIGN VIZUAL ---
st.markdown("""
    <style>
        .stApp { background-color: #2c0710; }
        [data-testid="stSidebar"] { background-color: #3d0a16; }
        h1 { color: #ff1a4d !important; font-family: 'Helvetica', sans-serif; font-weight: 300; }
        h2, h3, p, label, .stMarkdown { color: #ffccd5 !important; }
        .stTextInput > div > div > input, .stTextArea > div > div > textarea {
             background-color: #5e1223 !important; color: white !important; border: 1px solid #ff1a4d; }
        .stButton > button {
            background-color: #ff1a4d !important; color: white !important; border: none; box-shadow: 0 0 15px #ff1a4d; width: 100%; }
        .stButton > button:hover { background-color: #d9002f !important; }
