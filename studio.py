import streamlit as st
import requests
from io import BytesIO
from PIL import Image
import random
import time

# --- 1. CONFIGURARE PAGINĂ ---
st.set_page_config(page_title="Studio Design", page_icon="🎨", layout="centered")

# --- 2. DESIGN VIZUAL (Păstrăm tema Vișiniu/Neon, schimbăm doar numele) ---
st.markdown("""
    <style>
        /* Fundal Vișiniu Închis */
        .stApp { background-color: #2c0710; }
        [data-testid="stSidebar"] { background-color: #3d0a16; }
        
        /* Titluri și Text */
        h1 { 
            color: #ff1a4d !important; 
            text-shadow: 0 0 10px #ff0033; 
            font-family: 'Helvetica', sans-serif;
            font-weight: 300; /* Font mai subțire, mai elegant */
        }
        h2, h3, p, label, .stMarkdown, .stExpander { color: #ffccd5 !important; }
        
        /* Căsuțe de text și Butoane */
        .stTextInput > div > div > input, .stTextArea > div > div > textarea {
             background-color: #5e1223 !important; color: white !important; border: 1px solid #ff1a4d;
        }
        .stButton > button {
            background-color: #ff1a4d !important; color: white !important; border: none; box-shadow: 0 0 15px #ff1a4d;
        }
        .stButton > button:hover { background-color: #d9002f !important; }
        
        /* Metrici Tehnice */
        [data-testid="stMetricValue"] { color: #ff1a4d !important; }
        [data-testid="stMetricLabel"] { color: #ffccd5 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. INTERFAȚA UTILIZATOR ---
st.title("Studio Design") 
st.write("Generative AI • Inference Engine")

with st.sidebar:
    st.header("⚙️ Configurare")
    prompt_user = st.text_area("Descriere:", "Cyberpunk bmw m4, rain, neon lights")
    stil = st.selectbox("Stil:", ["Realistic", "3D Render", "Anime", "Digital Art"])
    
    # Selectorul de Server (Redundanță) - Foarte bun pt stabilitate
    server_choice = st.radio("Server Backend:", ["Server A (Turbo)", "Server B (Flux)"])
    
    st.markdown("---")
    buton = st.button("GENERARE IMAGINE")

# --- 4. LOGICA DE BACKEND (Safe Mode - Fără Plată) ---
if buton:
    with st.spinner("Se procesează cererea..."):
        try:
            start_time = time.time()
            numar_magic = random.randint(1, 999999)
            
            # Pregătire Prompt
            prompt_final = f"{prompt_user}, {stil} style"
            prompt_safe = prompt_final.replace(" ", "%20")
            
            # --- SELECTAREA MODELULUI ---
            if "Server A" in server_choice:
                # Turbo e cel mai rapid și stabil (Gratuit)
                model_n = "turbo"
            else:
                # Flux are calitate mai mare (uneori aglomerat)
                model_n = "flux"

            # URL STANDARD (Fără parametrii care declanșează plata)
            # Am scos setările de rezoluție forțată și nologo.
            url = f"https://image.pollinations.ai/prompt/{prompt_safe}?model={model_n}&seed={numar_magic}"
            
            # Header fals (Ca să nu fim blocați)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36'
            }
            
            raspuns = requests.get(url, headers=headers)
            
            durata = time.time() - start_time
            
            if raspuns.status_code == 200:
                image = Image.open(BytesIO(raspuns.content))
                st.image(image, caption=f"Rezultat ({model_n})", use_column_width=True)
                st.success("✅ Generare finalizată cu succes.")
                
                # METRICI PENTRU PROFESOR
                with st.expander("📊 Date Tehnice & Metrici (Click aici)"):
                    c1, c2, c3 = st.columns(3)
                    with c1: st.metric("Timp Inferență", f"{durata:.2f} s")
                    with c2: st.metric("Model Latent", model_n.capitalize())
                    with c3: st.metric("Seed", numar_magic)
            else:
                st.error("⚠️ Server ocupat. Încearcă să schimbi pe celălalt Server din meniul stânga!")
                
        except Exception as e:
            st.error(f"Eroare: {e}")
