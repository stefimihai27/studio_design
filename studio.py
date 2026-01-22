import streamlit as st
import random
import urllib.parse
import time

# --- 1. CONFIGURARE PAGINĂ ---
st.set_page_config(page_title="Studio Design", page_icon="🎨", layout="centered")

# --- 2. DESIGN VIZUAL (NEON-NOIR) ---
st.markdown("""
    <style>
        /* Fundal */
        .stApp { background-color: #2c0710; }
        [data-testid="stSidebar"] { background-color: #3d0a16; }
        
        /* Elemente Text */
        h1 { color: #ff1a4d !important; font-family: 'Helvetica', sans-serif; font-weight: 300; }
        h2, h3, p, label, .stMarkdown { color: #ffccd5 !important; }
        
        /* Controale */
        .stTextInput > div > div > input, .stTextArea > div > div > textarea {
             background-color: #5e1223 !important; color: white !important; border: 1px solid #ff1a4d; border-radius: 8px;
        }
        .stSelectbox > div > div > div {
             background-color: #5e1223 !important; color: white !important;
        }
        
        /* Buton */
        .stButton > button {
            background-color: #ff1a4d !important; color: white !important; border: none; 
            box-shadow: 0 0 15px #ff1a4d; width: 100%; font-weight: bold; padding: 12px;
        }
        .stButton > button:hover { background-color: #d9002f !important; box-shadow: 0 0 25px #ff1a4d; }
        
        /* Rezultat */
        .result-box {
            background-color: #3d0a16; padding: 15px; border-radius: 15px; 
            border: 1px solid #ff1a4d; text-align: center; margin-top: 20px;
        }
    </style>
    """, unsafe_allow_html=True)

# --- 3. INTERFAȚA ---
st.title("Studio Design") 
st.caption("System Status: ONLINE | Mode: Anti-Cache Direct Link")

with st.sidebar:
    st.header("⚙️ Configurare")
    prompt_user = st.text_area("Descriere:", "Cyberpunk bmw m4, neon lights, rain, 8k, realistic")
    stil = st.selectbox("Stil:", ["Photorealistic", "Cinematic", "Anime", "3D Render", "Oil Painting"])
    
    st.markdown("---")
    st.caption("ℹ️ Conexiune securizată fără cache.")
    buton = st.button("GENERARE IMAGINE")

# --- 4. LOGICA "CACHE-BUSTER" ---
if buton:
    # 1. Pregătire Prompt
    prompt_final = f"{prompt_user}, {stil} style, masterpiece, 8k resolution, highly detailed"
    prompt_encoded = urllib.parse.quote(prompt_final)
    
    # 2. Generare Seed (Aleatoriu)
    seed = random.randint(0, 1000000)
    
    # 3. TRUCUL MAGIC: Timestamp
    # Adăugăm timpul exact în milisecunde. Asta face link-ul UNIC în univers la fiecare secundă.
    # Browserul nu mai poate afișa eroarea veche din memorie.
    timestamp = int(time.time())
    
    # 4. Construim Link-ul
    # model=flux (Gratis)
    # nologo=false (Obligatoriu pentru gratis)
    # t={timestamp} (Sparge memoria Cache)
    # enhance=false (Reduce încărcarea serverului ca să nu primim erori)
    image_url = f"https://image.pollinations.ai/prompt/{prompt_encoded}?model=flux&width=1024&height=1024&seed={seed}&nologo=false&enhance=false&t={timestamp}"
    
    st.success("✅ Comandă trimisă! (Cache curățat automat)")
    
    # 5. Afișare Directă (HTML)
    st.markdown(
        f"""
        <div class="result-box">
            <h3 style="color: #ff1a4d;">Rezultat Generat</h3>
            <div style="display: flex; justify-content: center;">
                <img src="{image_url}" 
                     alt="Imaginea se încarcă..." 
                     width="100%" 
                     style="border-radius: 10px; min-height: 300px; background-color: #2c0710;"
                     onerror="this.style.display='none'; alert('Eroare de încărcare. Încearcă din nou.');"
                />
            </div>
            <p style="color: #ffccd5; margin-top: 10px; font-size: 0.8em;">
                ID Sesiune: {seed}-{timestamp} | Model: Flux
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
