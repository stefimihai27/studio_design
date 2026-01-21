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
            background-color: #ff1a4d !important; color: white !important; border: none; box-shadow: 0 0 15px #ff1a4d; width: 100%; }
        .stButton > button:hover { background-color: #d9002f !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("Studio Design") 
st.caption("Architecture: Hybrid Failover System")

with st.sidebar:
    st.header("⚙️ Configurare")
    prompt_user = st.text_area("Descriere:", "Cyberpunk bmw m4, neon lights, rain, 8k, realistic")
    stil = st.selectbox("Stil:", ["Photorealistic", "Cinematic", "Anime", "3D Render"])
    st.markdown("---")
    buton = st.button("GENERARE IMAGINE")

# --- 5. LOGICA PRINCIPALĂ ---
if buton:
    with st.spinner("Se caută cel mai bun server disponibil..."):
        prompt_final = f"{prompt_user}, {stil} style, 8k masterpiece"
        
        # PASUL 1: Încercăm Pollinations
        img, source = generate_with_pollinations(prompt_final)
        
        # PASUL 2: Dacă Pollinations dă eroare sau poza cu "Moved", intră Hugging Face
        if img is None:
            st.warning("⚠️ Serverul public este ocupat. Se comută pe serverul privat...")
            img, source = generate_with_huggingface(prompt_final)
        
        # AFIȘARE REZULTAT
        if img:
            st.image(img, caption=f"Generat cu succes ({source})", use_column_width=True)
            st.success("✅ Proces finalizat.")
        else:
            st.error("Toate serverele sunt extrem de aglomerate. Mai încearcă o dată în 10 secunde.")
