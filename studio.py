import streamlit as st
import requests
from io import BytesIO
from PIL import Image
import randomimport streamlit as st
import requests
from io import BytesIO
from PIL import Image
import random
import time

# --- 1. CONFIGURARE PAGINĂ ---
st.set_page_config(page_title="Neon Studio", page_icon="🔴", layout="centered")

# --- 2. DESIGN VISINIU & NEON (CSS) ---
st.markdown("""
    <style>
        /* Fundalul principal - Vișiniu închis */
        .stApp { background-color: #2c0710; }
        
        /* Meniul lateral */
        [data-testid="stSidebar"] { background-color: #3d0a16; }

        /* Titluri cu efect Neon */
        h1 {
            color: #ff1a4d !important;
            text-shadow: 0 0 10px #ff0033, 0 0 20px #ff0033;
        }
        
        /* Text obișnuit */
        h2, h3, p, label, .stMarkdown { color: #ffccd5 !important; }

        /* Căsuțele de text */
        .stTextInput > div > div > input, .stTextArea > div > div > textarea {
             background-color: #5e1223 !important;
             color: white !important;
             border: 1px solid #ff1a4d;
        }
        
        /* Butonul */
        .stButton > button {
            background-color: #ff1a4d !important;
            color: white !important;
            border: none;
            box-shadow: 0 0 15px #ff1a4d;
            font-weight: bold;
        }
        .stButton > button:hover { background-color: #d9002f !important; }
        
        /* Mesajele de eroare/succes */
        .stAlert { background-color: #3d0a16; color: white; border: 1px solid #ff1a4d; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. INTERFAȚA ---
st.title("🔴 NEON DESIGN STUDIO")
st.write("Style: Cyberpunk • Status: Online")

with st.sidebar:
    st.header("⚙️ CONTROL PANEL")
    prompt_user = st.text_area("Descrie ideea ta:", "Un BMW M4 futurist, lumini roșii, ploaie, noaptea")
    stil = st.selectbox("Stil Vizual:", ["Photorealistic", "Cyberpunk", "Anime", "3D Render", "Oil Painting"])
    st.markdown("---")
    buton = st.button("✨ ACTIVEAZĂ GENERAREA ✨")

# --- 4. LOGICA DE GENERARE (CU PROTECȚIE) ---
if buton:
    with st.spinner("🔴 Se stabilește conexiunea securizată..."):
        try:
            # A. Generăm numere unice ca să păcălim cache-ul serverului
            numar_magic = random.randint(1, 999999999)
            
            # B. Construim promptul
            prompt_final = f"{prompt_user}, {stil} style, highly detailed, 8k"
            prompt_safe = prompt_final.replace(" ", "%20")
            
            # C. URL SIMPLIFICAT (Fără funcții PRO care cer bani)
            # Am scos 'nologo' și rezoluția forțată care dau erori
            url = f"https://image.pollinations.ai/prompt/{prompt_safe}?model=flux&seed={numar_magic}"
            
            # D. TRUCUL SUPREM: HEADER FALS
            # Asta îi spune serverului că suntem un browser Chrome, nu un script Python
            headers_falsi = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            # E. Facem cererea cu "deghizarea" activată
            raspuns = requests.get(url, headers=headers_falsi)
            
            if raspuns.status_code == 200:
                image = Image.open(BytesIO(raspuns.content))
                st.image(image, caption="Imagine Generată", use_column_width=True)
                st.success("✅ Proces complet.")
            else:
                st.warning("⚠️ Trafic intens. Mai apasă o dată butonul în 10 secunde.")
                
        except Exception as e:
            st.error(f"Eroare sistem: {e}")
import time  # <--- Am adus intăriri pentru a evita blocarea

# --- CONFIGURARE PAGINĂ ---
st.set_page_config(page_title="Neon Studio", page_icon="🔴", layout="centered")

# --- DESIGN PERSONALIZAT (CSS) ---
# Aici e doar machiajul site-ului (Vișiniu + Neon). Nu afectează pozele!
st.markdown("""
    <style>
        /* Fundalul principal */
        .stApp { background-color: #2c0710; }
        
        /* Sidebar-ul */
        [data-testid="stSidebar"] { background-color: #3d0a16; }

        /* Titlurile - Roșu Neon */
        h1 {
            color: #ff1a4d !important;
            text-shadow: 0 0 15px #ff0033;
        }
        
        /* Textul normal - Roz pal */
        h2, h3, p, label, .stMarkdown { color: #ffccd5 !important; }

        /* Căsuțele de text */
        .stTextInput > div > div > input, .stTextArea > div > div > textarea {
             background-color: #5e1223 !important;
             color: white !important;
             border: 1px solid #ff1a4d;
        }
        
        /* Butonul */
        .stButton > button {
            background-color: #ff1a4d !important;
            color: white !important;
            border: none;
            box-shadow: 0 0 10px #ff1a4d;
        }
        .stButton > button:hover { background-color: #d9002f !important; }
    </style>
    """, unsafe_allow_html=True)

# --- APLICAȚIA ---

st.title("🔴 NEON DESIGN STUDIO")
st.write("Interfață Cyberpunk • Generare Nelimitată")

with st.sidebar:
    st.header("CONTROL PANEL")
    prompt_user = st.text_area("Descrie ideea ta:", "Un BMW albastru pe plajă")
    
    # Am simplificat meniul ca să nu încurce
    stil = st.selectbox("Stil (Opțional):", ["Realist (4k)", "Anime", "Cyberpunk", "Pictură Ulei", "3D Render"])
    
    st.markdown("---")
    buton = st.button("✨ ACTIVEAZĂ GENERAREA ✨")

if buton:
    with st.spinner("🔴 Se procesează..."):
        try:
            # --- SOLUȚIA ANTI-BLOCAJ ---
            # Combinăm un număr imens cu ora exactă. E imposibil să se repete.
            numar_magic = random.randint(1, 9999999)
            timp_exact = int(time.time())
            
            # --- SOLUȚIA PENTRU CULORI ---
            # Construim promptul FĂRĂ să adăugăm "red neon" forțat.
            prompt_final = f"{prompt_user}, {stil} style, detailed, 8k"
            prompt_safe = prompt_final.replace(" ", "%20")
            
            # Link-ul include acum și timpul (&t=...)
            url = f"https://image.pollinations.ai/prompt/{prompt_safe}?width=1024&height=1024&seed={numar_magic}&t={timp_exact}&nologo=true"
            
            raspuns = requests.get(url)
            
            if raspuns.status_code == 200:
                image = Image.open(BytesIO(raspuns.content))
                st.image(image, caption="Design Generat", use_column_width=True)
                st.success("✅ Generare reușită!")
            else:
                st.error("⚠️ Eroare server. Mai apasă o dată!")
                
        except Exception as e:
            st.error(f"Eroare: {e}")

