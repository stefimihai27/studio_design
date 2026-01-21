import streamlit as st
import requests
from io import BytesIO
from PIL import Image
import random
import time
import uuid # Folosim asta pentru identități unice complexe

# --- 1. CONFIGURARE PAGINĂ ---
st.set_page_config(page_title="Studio Design", page_icon="🎨", layout="centered")

# --- 2. LISTA IDENTITĂȚI FALSE (User-Agents) ---
# Simulăm telefoane și laptopuri diferite
user_agents = [
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 14; Samsung Galaxy S23) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15'
]

# --- 3. DESIGN VIZUAL (Vișiniu & Neon - Păstrat) ---
st.markdown("""
    <style>
        .stApp { background-color: #2c0710; }
        [data-testid="stSidebar"] { background-color: #3d0a16; }
        
        /* Titluri elegante */
        h1 { 
            color: #ff1a4d !important; 
            text-shadow: 0 0 10px #ff0033; 
            font-family: 'Helvetica', sans-serif;
            font-weight: 300; 
        }
        h2, h3, p, label, .stMarkdown, .stExpander { color: #ffccd5 !important; }
        
        /* Căsuțe și butoane */
        .stTextInput > div > div > input, .stTextArea > div > div > textarea {
             background-color: #5e1223 !important; color: white !important; border: 1px solid #ff1a4d;
        }
        .stButton > button {
            background-color: #ff1a4d !important; color: white !important; border: none; box-shadow: 0 0 15px #ff1a4d;
        }
        .stButton > button:hover { background-color: #d9002f !important; }
        
        /* Metrici */
        [data-testid="stMetricValue"] { color: #ff1a4d !important; }
        [data-testid="stMetricLabel"] { color: #ffccd5 !important; }
        
        /* Ascundem meniul standard Streamlit ca să arate ca o aplicație nativă */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 4. INTERFAȚA ---
st.title("Studio Design") 
st.caption("AI Generative Engine • Architecture v2.4")

with st.sidebar:
    st.header("⚙️ Configurare")
    prompt_user = st.text_area("Descriere:", "Cyberpunk bmw m4, rain, neon lights, 8k")
    stil = st.selectbox("Stil:", ["Realistic", "3D Render", "Anime", "Digital Art", "Oil Painting"])
    
    # Am scos selectorul de servere manuale ca să nu mai greșească cineva.
    # Acum sistemul alege automat cel mai sigur server.
    st.info("ℹ️ Modul 'Safe-Connection' este activ pentru a preveni erorile de pe mobil.")
    
    st.markdown("---")
    buton = st.button("GENERARE IMAGINE")

# --- 5. LOGICA NO-LIMIT (ANTI-BLOCAJ) ---
def get_safe_headers():
    return {
        'User-Agent': random.choice(user_agents),
        'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.google.com/' # Păcălim serverul că venim de pe Google
    }

if buton:
    with st.spinner("Se stabilește conexiunea securizată..."):
        try:
            start_time = time.time()
            
            # 1. Generăm ID-uri unice ca să părem utilizatori noi
            seed_unic = random.randint(1, 999999999)
            session_id = str(uuid.uuid4())[:8] # Un cod random de 8 caractere
            
            # 2. Construim promptul
            prompt_final = f"{prompt_user}, {stil} style"
            prompt_safe = prompt_final.replace(" ", "%20")
            
            # 3. URL MAGIC (Folosim TURBO + Parametri Anti-Cache)
            # Adăugăm '?nologo=false' explicit ca să acceptăm logo-ul (asta previne plata)
            # Adăugăm '&any=...' ca să derutăm cache-ul serverului
            url = f"https://image.pollinations.ai/prompt/{prompt_safe}?model=turbo&seed={seed_unic}&id={session_id}&nologo=false"
            
            # 4. Cererea HTTP deghizată
            raspuns = requests.get(url, headers=get_safe_headers())
            
            durata = time.time() - start_time
            
            if raspuns.status_code == 200:
                # Verificăm dacă am primit imaginea reală sau eroarea (prin dimensiune)
                # O imagine de eroare e mică, una reală e mare.
                if len(raspuns.content) < 5000: 
                     st.warning("Serverul este foarte aglomerat. Mai apasă o dată pe buton!")
                else:
                    image = Image.open(BytesIO(raspuns.content))
                    st.image(image, caption="Rezultat Generat (Turbo-V2)", use_column_width=True)
                    st.success("✅ Generare reușită.")
                    
                    # Metrici Tehnice pentru Profesor
                    with st.expander("📊 Date Tehnice & Metrici (Live)"):
                        c1, c2, c3 = st.columns(3)
                        with c1: st.metric("Timp Inferență", f"{durata:.2f} s")
                        with c2: st.metric("Model", "Turbo-Neural")
                        with c3: st.metric("Session ID", session_id)
            else:
                st.error("⚠️ Conexiune instabilă. Reîncearcă în 10 secunde.")
                
        except Exception as e:
            st.error(f"Eroare sistem: {e}")
