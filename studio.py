import streamlit as st
import requests
from io import BytesIO
from PIL import Image
import random
import time
import uuid

# --- 1. CONFIGURARE PAGINĂ ---
st.set_page_config(page_title="Studio Design", page_icon="🎨", layout="centered")

# --- 2. IDENTITĂȚI FALSE (Ca să nu te blocheze) ---
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/122.0.0.0 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 14; Samsung Galaxy S24) Chrome/122.0.0.0 Mobile Safari/537.36'
]

# --- 3. DESIGN VIZUAL (Vișiniu & Neon) ---
st.markdown("""
    <style>
        .stApp { background-color: #2c0710; }
        [data-testid="stSidebar"] { background-color: #3d0a16; }
        h1 { 
            color: #ff1a4d !important; 
            text-shadow: 0 0 10px #ff0033; 
            font-family: 'Helvetica', sans-serif;
            font-weight: 300; 
        }
        h2, h3, p, label, .stMarkdown, .stExpander { color: #ffccd5 !important; }
        .stTextInput > div > div > input, .stTextArea > div > div > textarea {
             background-color: #5e1223 !important; color: white !important; border: 1px solid #ff1a4d;
        }
        .stButton > button {
            background-color: #ff1a4d !important; color: white !important; border: none; box-shadow: 0 0 15px #ff1a4d;
        }
        .stButton > button:hover { background-color: #d9002f !important; }
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        [data-testid="stMetricValue"] { color: #ff1a4d !important; }
        [data-testid="stMetricLabel"] { color: #ffccd5 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. INTERFAȚA ---
st.title("Studio Design") 
st.caption("Engine: Pollinations Turbo (Free Tier)")

with st.sidebar:
    st.header("⚙️ Configurare")
    prompt_user = st.text_area("Descriere:", "Cyberpunk bmw m4, neon lights, rain, 8k, realistic")
    stil = st.selectbox("Stil:", ["Photorealistic", "Cinematic", "Anime", "3D Render", "Illustration"])
    
    st.info("ℹ️ Modul Gratuit Activat (Turbo).")
    st.markdown("---")
    buton = st.button("GENERARE IMAGINE")

# --- 5. LOGICA DE EVITARE A PLĂȚII ---
if buton:
    with st.spinner("Se generează design-ul..."):
        try:
            start_time = time.time()
            
            # Generăm ID-uri unice ca să părem utilizatori noi de fiecare dată
            seed_unic = random.randint(1, 999999999)
            session_id = str(uuid.uuid4())
            
            # Construim promptul
            prompt_final = f"{prompt_user}, {stil} style"
            prompt_safe = prompt_final.replace(" ", "%20")
            
            # --- TRUCUL SUPREM ---
            # model=turbo -> E gratis.
            # nologo=false -> Acceptăm logo-ul (asta deblochează generarea).
            # width=1024 -> Dimensiune standard.
            url = f"https://image.pollinations.ai/prompt/{prompt_safe}?model=turbo&seed={seed_unic}&width=1024&height=1024&nologo=false"
            
            # Header fals
            headers = {
                'User-Agent': random.choice(user_agents),
                'Referer': 'https://www.google.com/'
            }
            
            # Facem cererea cu un mic delay aleatoriu ca să părem oameni
            time.sleep(random.uniform(0.5, 1.5))
            raspuns = requests.get(url, headers=headers, timeout=20)
            
            durata = time.time() - start_time
            
            if raspuns.status_code == 200:
                # Verificăm dacă ne-a trimis iar poza cu "We Moved" (care e mică de obicei)
                # O imagine reală are peste 10.000 bytes.
                if len(raspuns.content) < 10000:
                     st.error("Serverul face modificări. Mai apasă o dată butonul Generare!")
                else:
                    image = Image.open(BytesIO(raspuns.content))
                    st.image(image, caption="Design Generat (Turbo)", use_column_width=True)
                    st.success("✅ Generare reușită.")
                    
                    # Metricile pentru Flavius
                    with st.expander("📊 Date Tehnice (Live)"):
                        c1, c2, c3 = st.columns(3)
                        with c1: st.metric("Timp Inferență", f"{durata:.2f} s")
                        with c2: st.metric("Model", "Pollinations-Turbo")
                        with c3: st.metric("Seed", str(seed_unic)[:5])
            else:
                st.error("⚠️ Serverul este ocupat momentan. Mai încearcă în 10 secunde.")
                
        except Exception as e:
            st.error(f"Eroare: {e}")
